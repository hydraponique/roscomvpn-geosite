#!/usr/bin/env python3
"""
Скрипт удаляет домены из geosite-файла, если они указывают
только на IP-адреса, которые уже есть в списке geoip:direct/geoip:whitelist.

Проверка выполняется через DNS-серверы в разных странах (check-host.net).
Если все серверы подтвердили, что домен ведёт на IP из direct — домен удаляется.

Использование:
  python3 deduplicate_geoip.py data/category-ru
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import struct
import subprocess
import time
from bisect import bisect_right
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ссылка на файл со списком IP-диапазонов (direct.txt или whitelist.txt) в GitHub
DIRECT_TXT_URL = "https://raw.githubusercontent.com/hydraponique/roscomvpn-geoip/release/text/direct.txt"

# Адрес API для проверки DNS
API_BASE = "https://check-host.net"

# Серверы в России для проверки DNS
RU_NODES = [
    "ru1.node.check-host.net",
    "ru2.node.check-host.net",
    "ru3.node.check-host.net",
]

# Зарубежные серверы для проверки DNS.
# В каждой группе первый сервер — основной, остальные — запасные.
FOREIGN_NODES = [
    ["de1.node.check-host.net", "de4.node.check-host.net"],
    ["us1.node.check-host.net", "us2.node.check-host.net", "us3.node.check-host.net", "us4.node.check-host.net"],
    ["se1.node.check-host.net", "se2.node.check-host.net"],
]

# Пауза между попытками опроса результата (секунды)
POLL_INTERVAL = 1
# Сколько раз опрашивать результат
POLL_MAX_ATTEMPTS = 5
# Сколько доменов проверять одновременно
WORKERS = 8


# ── Скачивание и работа с IP-диапазонами ──────────────────────────────────

def curl_get(url: str, timeout: int = 5) -> str:
    """Скачивает содержимое по ссылке через curl и возвращает текст."""
    result = subprocess.run(
        ["curl", "-fsSL", "--retry", "3", "--retry-delay", "1", "--max-time", str(timeout), url],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def curl_json(url: str) -> dict | None:
    """Скачивает JSON по ссылке через curl. При ошибке повторяет до 3 раз."""
    result = subprocess.run(
        ["curl", "-fsSL", "--retry", "3", "--retry-delay", "1", "--max-time", "5",
         "-H", "Accept: application/json", url],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def load_direct_cidrs_from_url() -> tuple[list[tuple[int, int]], list[int]]:
    """Скачивает direct.txt/whitelist.txt и разбирает IP-диапазоны прямо из памяти.
    Возвращает отсортированный список диапазонов и список их начал (для быстрого поиска)."""
    print(f"Downloading direct.txt from {DIRECT_TXT_URL} ...")
    data = curl_get(DIRECT_TXT_URL)
    print(f"  Скачано {len(data)} байт")

    intervals: list[tuple[int, int]] = []
    for line in data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
        except ValueError:
            continue
        if net.version == 4:
            intervals.append((int(net.network_address), int(net.broadcast_address)))
    intervals.sort()
    starts = [iv[0] for iv in intervals]
    return intervals, starts


def ip_to_int(ip_str: str) -> int | None:
    """Быстро превращает IPv4-строку в число. Возвращает None если формат не IPv4."""
    parts = ip_str.split(".")
    if len(parts) != 4:
        return None
    try:
        return struct.unpack("!I", bytes(int(p) for p in parts))[0]
    except (ValueError, struct.error):
        return None


def ip_in_direct(ip_str: str, intervals: list[tuple[int, int]], starts: list[int]) -> bool:
    """Проверяет, входит ли IP-адрес в один из диапазонов direct.
    Использует быстрый поиск по отсортированному списку."""
    val = ip_to_int(ip_str)
    if val is None:
        return False
    idx = bisect_right(starts, val) - 1
    if idx < 0:
        return False
    return intervals[idx][0] <= val <= intervals[idx][1]


# ── Работа с API check-host.net ──────────────────────────────────────────

def check_dns(domain: str, nodes: list[str]) -> str | None:
    """Отправляет запрос на проверку DNS домена через указанные серверы.
    Возвращает идентификатор запроса или None при ошибке."""
    node_params = "&".join(f"node={n}" for n in nodes)
    url = f"{API_BASE}/check-dns?host={domain}&{node_params}"
    try:
        data = curl_json(url)
        return data.get("request_id") if data else None
    except Exception:
        return None


def poll_results(request_id: str, nodes: list[str]) -> dict | None:
    """Ждёт, пока все серверы вернут результат проверки DNS.
    Если не все ответили за отведённое время — возвращает то, что есть."""
    url = f"{API_BASE}/check-result/{request_id}"
    last_data = None
    for _ in range(POLL_MAX_ATTEMPTS):
        time.sleep(POLL_INTERVAL)
        try:
            data = curl_json(url)
        except Exception:
            continue
        if data:
            last_data = data
            if all(data.get(n) is not None for n in nodes):
                return data
    return last_data


def extract_a_records(node_result) -> list[str] | None:
    """Достаёт IPv4-адреса (A-записи) из ответа одного сервера.
    Возвращает список IP или None, если записей нет."""
    if not isinstance(node_result, list):
        return None
    ips: list[str] = []
    for entry in node_result:
        if isinstance(entry, dict) and "A" in entry:
            ips.extend(entry["A"])
    return ips or None


def try_fallback_group(domain: str, group: list[str]) -> tuple[str, list[str] | None] | None:
    """Пробует запасные серверы из группы по очереди.
    Возвращает (имя сервера, список IP) или None, если никто не ответил."""
    for fallback in group[1:]:
        fb_id = check_dns(domain, [fallback])
        if not fb_id:
            continue
        fb_results = poll_results(fb_id, [fallback])
        if fb_results and fb_results.get(fallback) is not None:
            return fallback, extract_a_records(fb_results.get(fallback))
    return None


def resolve_domain(domain: str) -> dict[str, list[str] | None]:
    """Проверяет DNS домена на всех серверах (РФ и зарубежных).
    Если основной зарубежный сервер не ответил — пробует запасные параллельно.
    Возвращает словарь: имя сервера → список IP (или None, если домен не найден)."""

    # Сначала отправляем один общий запрос на все основные серверы
    primary_foreign = [group[0] for group in FOREIGN_NODES]
    all_primary = RU_NODES + primary_foreign

    request_id = check_dns(domain, all_primary)
    if not request_id:
        return {}

    results = poll_results(request_id, all_primary)
    if not results:
        return {}

    node_ips: dict[str, list[str] | None] = {}

    # Собираем ответы от российских серверов
    for node in RU_NODES:
        if results.get(node) is not None:
            node_ips[node] = extract_a_records(results.get(node))

    # Собираем ответы от зарубежных серверов.
    # Если основной не ответил — запускаем запасные параллельно.
    groups_needing_fallback = []
    for group in FOREIGN_NODES:
        primary = group[0]
        if results.get(primary) is not None:
            node_ips[primary] = extract_a_records(results.get(primary))
        else:
            groups_needing_fallback.append(group)

    if groups_needing_fallback:
        with ThreadPoolExecutor(max_workers=len(groups_needing_fallback)) as pool:
            futures = {
                pool.submit(try_fallback_group, domain, group): group
                for group in groups_needing_fallback
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    node_name, ips = result
                    node_ips[node_name] = ips

    return node_ips


# ── Разбор строк geosite-файла ────────────────────────────────────────────

# Регулярка для удаления комментариев и атрибутов из строки (всё после @, # или //)
_INLINE_STRIP = re.compile(r"\s*[@#].*|[ \t]*//.*")


def parse_entry(line: str) -> tuple[str | None, str | None]:
    """Разбирает строку geosite-файла. Если строка содержит domain: или full: —
    возвращает (тип, домен). Иначе возвращает (None, None)."""
    s = line.strip()
    if not s or s.startswith("#") or s.startswith("//"):
        return None, None
    s = _INLINE_STRIP.sub("", s).strip()
    if s.startswith("domain:"):
        return "domain", s[7:].lstrip(".")
    if s.startswith("full:"):
        return "full", s[5:].lstrip(".")
    return None, None


# ── Проверка одного домена ─────────────────────────────────────────────────

def classify_node(ips: list[str] | None, tag: str,
                  intervals: list[tuple[int, int]], starts: list[int],
                  detail_parts: list[str]) -> str:
    """Классифицирует ответ одного сервера: 'nxdomain', 'direct', 'outside'.
    Добавляет описание в detail_parts."""
    if ips is None:
        detail_parts.append(f"{tag}=NXDOMAIN")
        return "nxdomain"
    all_in = all(ip_in_direct(ip, intervals, starts) for ip in ips)
    if all_in:
        detail_parts.append(f"{tag}=direct({','.join(ips)})")
        return "direct"
    outside = [ip for ip in ips if not ip_in_direct(ip, intervals, starts)]
    detail_parts.append(f"{tag}=OUTSIDE({','.join(outside)})")
    return "outside"


def check_one_domain(
    idx: int, pfx: str, domain: str,
    intervals: list[tuple[int, int]], starts: list[int],
) -> tuple[int, str, str, bool]:
    """Проверяет один домен. Весь вывод собирается в строку (не печатается).
    Возвращает (номер строки, заголовок, текст лога, нужно ли удалять)."""
    header = f"{pfx}:{domain}"

    node_ips = resolve_domain(domain)
    if not node_ips:
        return idx, header, "  → KEEP (API error)", False

    nodes_ok = 0
    nodes_nxdomain = 0
    nodes_outside = 0
    ru_missing = 0
    foreign_missing = 0
    detail_parts: list[str] = []

    # Проверяем ответы российских серверов (с ранним выходом при OUTSIDE)
    for node in RU_NODES:
        if node not in node_ips:
            ru_missing += 1
            detail_parts.append(f"{node.split('.')[0]}=NO_RESP")
            continue
        kind = classify_node(node_ips[node], node.split(".")[0], intervals, starts, detail_parts)
        if kind == "direct":
            nodes_ok += 1
        elif kind == "nxdomain":
            nodes_nxdomain += 1
        else:
            nodes_outside += 1
            break  # уже точно KEEP — дальше проверять не нужно

    # Проверяем ответы зарубежных серверов (если ещё не нашли OUTSIDE)
    if nodes_outside == 0:
        for group in FOREIGN_NODES:
            node = next((n for n in group if n in node_ips), None)
            if node is None:
                foreign_missing += 1
                detail_parts.append(f"{group[0].split('.')[0]}=NO_RESP")
                continue
            tag = node.split(".")[0]
            kind = classify_node(node_ips[node], tag, intervals, starts, detail_parts)
            if kind == "direct":
                nodes_ok += 1
            elif kind == "nxdomain":
                nodes_nxdomain += 1
            else:
                nodes_outside += 1
                break  # уже точно KEEP

    detail = "  ".join(detail_parts)
    responded = nodes_ok + nodes_nxdomain + nodes_outside

    # Принятие решения:
    # - Должны ответить минимум 1 российский и 2 зарубежных сервера
    # - Если хоть один сервер нашёл IP вне direct — оставляем домен
    # - Если все ответившие серверы дали direct или NXDOMAIN — удаляем
    ru_responded = len(RU_NODES) - ru_missing
    foreign_responded = len(FOREIGN_NODES) - foreign_missing
    if nodes_outside > 0:
        return idx, header, f"  → KEEP    [{nodes_ok}/{responded} direct]  {detail}", False
    if ru_responded < 1 or foreign_responded < 2:
        return idx, header, f"  → KEEP    [insufficient responses]  {detail}", False
    if nodes_ok > 0 or nodes_nxdomain == responded:
        return idx, header, f"  → REMOVE  [{nodes_ok} direct, {nodes_nxdomain} nxdomain / {responded} responded]  {detail}", True
    return idx, header, f"  → KEEP    [{nodes_ok}/{responded} direct]  {detail}", False


# ── Основная логика ────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Deduplicate geosite domains covered by geoip:direct/geoip:whitelist")
    ap.add_argument("geosite_file", help="Geosite data file (e.g. data/category-ru, data/whitelist)")
    ap.add_argument("--workers", type=int, default=WORKERS, help=f"Parallel workers (default: {WORKERS})")
    args = ap.parse_args()

    # Шаг 1. Скачиваем и разбираем список IP-диапазонов (direct.txt/whitelist.txt)
    intervals, starts = load_direct_cidrs_from_url()
    print(f"  {len(intervals)} IPv4 CIDR ranges loaded")

    total_nodes = len(RU_NODES) + len(FOREIGN_NODES)
    print(f"  {total_nodes} check nodes ({len(RU_NODES)} RU + {len(FOREIGN_NODES)} foreign)")
    print(f"  {args.workers} parallel workers")

    # Шаг 2. Читаем geosite-файл и выбираем строки с domain:/full:
    with open(args.geosite_file, encoding="utf-8") as f:
        lines = f.readlines()

    entries: list[tuple[int, str, str]] = []  # (номер строки, тип, домен)
    for i, line in enumerate(lines):
        pfx, dom = parse_entry(line)
        if pfx and dom:
            entries.append((i, pfx, dom))

    total = len(entries)
    print(f"  {total} domain/full entries to check (keyword/regexp skipped)\n")

    # Шаг 3. Проверяем домены параллельно через DNS-серверы
    to_remove: set[int] = set()

    # Собираем все результаты, потом выводим в исходном порядке
    results: dict[int, tuple[int, str, str, bool]] = {}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(check_one_domain, idx, pfx, domain, intervals, starts): seq
            for seq, (idx, pfx, domain) in enumerate(entries)
        }
        done = 0
        for future in as_completed(futures):
            done += 1
            seq = futures[future]
            results[seq] = future.result()
            # Показываем прогресс (номер без деталей, детали потом)
            print(f"\r  Progress: {done}/{total}", end="", flush=True)

    print()  # новая строка после прогресса

    # Выводим результаты в исходном порядке
    for seq in range(total):
        line_idx, header, log_line, should_remove = results[seq]
        print(f"[{seq+1}/{total}] {header}")
        print(log_line)
        if should_remove:
            to_remove.add(line_idx)

    # Шаг 4. Выводим итоги
    print(f"\n{'='*60}")
    print(f"Total checked : {total}")
    print(f"To remove     : {len(to_remove)}")
    print(f"Kept          : {total - len(to_remove)}")

    if to_remove:
        print("\nRemoved entries:")
        for idx in sorted(to_remove):
            print(f"  L{idx+1}: {lines[idx].rstrip()}")

    # Шаг 5. Записываем результат (без удалённых строк)
    with open(args.geosite_file, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            if i not in to_remove:
                f.write(line)

    print(f"\nWritten → {args.geosite_file}")


if __name__ == "__main__":
    main()
