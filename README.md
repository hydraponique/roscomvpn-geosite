<div align="center">

<table width="100%">
<tr>
<td align="center"><a href="https://github.com/hydraponique/roscomvpn-geoip">RoscomVPN GeoIP</a></td>
<td align="center"><a href="https://github.com/hydraponique/roscomvpn-geosite"><b>🌐 RoscomVPN Geosite</b></a></td>
<td align="center"><a href="https://github.com/hydraponique/roscomvpn-routing">RoscomVPN Routing</a></td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/github/downloads/hydraponique/roscomvpn-geoip/total.svg" alt="Downloads"> <img src="https://data.jsdelivr.com/v1/package/gh/hydraponique/roscomvpn-geoip/badge" alt="jsDelivr"></td>
<td align="center"><img src="https://img.shields.io/github/downloads/hydraponique/roscomvpn-geosite/total.svg" alt="Downloads"> <img src="https://data.jsdelivr.com/v1/package/gh/hydraponique/roscomvpn-geosite/badge" alt="jsDelivr"></td>
<td align="center"><img src="https://img.shields.io/github/stars/hydraponique/roscomvpn-routing.svg" alt="Stars"> <img src="https://img.shields.io/badge/Happ-blue.svg" alt="Happ"> <img src="https://img.shields.io/badge/Mihomo-grey.svg" alt="Mihomo"> <img src="https://img.shields.io/badge/Incy-darkgreen.svg" alt="Incy"></td>
</tr>
</table>

# 🌐 RoscomVPN Geosite

**Генерирует `geosite.dat` и рулсеты для Mihomo/sing-box**
**с категоризированными списками доменов для маршрутизации трафика РФ/РБ**

</div>

---

## 📥 Форматы и скачивание

<details open>
<summary><b>geosite.dat (V2Ray/Xray)</b></summary>

<table width="100%">
<thead><tr><th align="left">Источник</th><th align="left">Ссылка</th></tr></thead>
<tbody>
<tr><td>🔗 GitHub Releases</td><td><a href="https://github.com/hydraponique/roscomvpn-geosite/releases/latest/download/geosite.dat">https://github.com/hydraponique/roscomvpn-geosite/releases/latest/download/geosite.dat</a></td></tr>
<tr><td>⚡ jsDelivr CDN</td><td><a href="https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/geosite.dat">https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/geosite.dat</a></td></tr>
</tbody>
</table>

</details>

<details>
<summary><b>🔶 Mihomo (.mrs) и 🟣 sing-box (.srs)</b></summary>

<table width="100%">
<thead><tr><th align="left">Формат</th><th align="left">Шаблон ссылки</th></tr></thead>
<tbody>
<tr><td>🔶 Mihomo (.mrs)</td><td><a href="https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/mihomo/">https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/mihomo/{категория}.mrs</a></td></tr>
<tr><td>🟣 sing-box (.srs)</td><td><a href="https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/sing-box/">https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/sing-box/{категория}.srs</a></td></tr>
</tbody>
</table>

</details>

---

## 📋 Категории

### 🇷🇺 Россия

<table width="100%">
<thead><tr><th align="left">Категория</th><th align="left">Описание</th><th align="left">Назначение</th></tr></thead>
<tbody>
<tr><td><code>whitelist</code></td><td>Белый список доменов</td><td>Обязательный список в любом случае, direct</td></tr>
<tr><td><code>category-ru</code></td><td>Российские домены и сервисы</td><td>Расширение для whitelist, используется для не-БС хостов, direct</td></tr>
<tr><td><code>category-geoblock-ru</code></td><td>Геоблокированный RU контент</td><td>Серверная маршрутизация РУ сервер->Зарубеж</td></tr>
</tbody>
</table>

### 🌍 Сервисы

<table width="100%">
<thead><tr><th align="left">Категория</th><th align="left">Описание</th><th align="left">Назначение</th></tr></thead>
<tbody>
<tr><td><code>apple</code></td><td>Apple сервисы</td><td>В direct, фикс пуш-уведомлений</td></tr>
<tr><td><code>google-play</code></td><td>Google Play</td><td>В proxy, ТСПУ</td></tr>
<tr><td><code>google-deepmind</code></td><td>Google DeepMind / AI</td><td>Серверная маршрутизация РУ сервер->Зарубеж</td></tr>
<tr><td><code>microsoft</code></td><td>Microsoft сервисы</td><td>В direct, экономия трафика, фикс пушей</td></tr>
<tr><td><code>github</code></td><td>GitHub</td><td>Proxy, Борьба с ТСПУ и банами РКН</td></tr>
<tr><td><code>telegram</code></td><td>Telegram</td><td>Proxy, Борьба с ТСПУ и банами РКН</td></tr>
<tr><td><code>youtube</code></td><td>YouTube</td><td>Proxy, Борьба с ТСПУ и банами РКН</td></tr>
<tr><td><code>twitch</code></td><td>Twitch</td><td>Все домены twitch, если есть twitch-ads - в direct</td></tr>
<tr><td><code>twitch-ads</code></td><td>Twitch</td><td>Отключает рекламу, поднимает качество до 1080p+ - только в proxy</td></tr>
<tr><td><code>pinterest</code></td><td>Pinterest</td><td>Убираем рекламу на сервисе, direct</td></tr>
</tbody>
</table>

### 🎮 Игры

<table width="100%">
<thead><tr><th align="left">Категория</th><th align="left">Описание</th><th align="left">Назначение</th></tr></thead>
<tbody>
<tr><td><code>steam</code></td><td>Steam</td><td>В direct, экономия трафика, снижение пинга</td></tr>
<tr><td><code>epic-games</code></td><td>Epic Games Store</td><td>В direct, экономия трафика, снижение пинга</td></tr>
<tr><td><code>riot</code></td><td>Riot Games (LoL, Valorant)</td><td>В direct, экономия трафика, снижение пинга</td></tr>
<tr><td><code>escapefromtarkov</code></td><td>Escape from Tarkov</td><td>В direct, нужен для входа в любой гео-аккаунт в игре</td></tr>
<tr><td><code>faceit</code></td><td>FaceIT</td><td>В direct, расширяет список доступных серверов сервиса</td></tr>
</tbody>
</table>

### ⚙️ Прочее

<table width="100%">
<thead><tr><th align="left">Категория</th><th align="left">Описание</th><th align="left">Назначение</th></tr></thead>
<tbody>
<tr><td><code>category-ads</code></td><td>Рекламные домены</td><td>В block, реклама в VK/Mail.Ru</td></tr>
<tr><td><code>win-spy</code></td><td>Windows телеметрия/слежка (~377)</td><td>В block, слежка</td></tr>
<tr><td><code>private</code></td><td>Приватные/внутренние сети</td><td>Только директ, обязательный</td></tr>
<tr><td><code>torrent</code></td><td>Торрент-трекеры и DHT</td><td>Блок, работает не на 100%</td></tr>
</tbody>
</table>

---

## 🛠 Использование с Xray/V2Ray

```json
{
  "routing": {
    "rules": [
      {
        "type": "field",
        "domain": ["geosite:category-ru"],
        "outboundTag": "direct"
      },
      {
        "type": "field",
        "domain": ["geosite:win-spy"],
        "outboundTag": "block"
      }
    ]
  }
}
```

---

## 🔧 Инструменты сборки

- [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) — компилятор geosite.dat для Xray
- [Mihomo](https://github.com/MetaCubeX/mihomo) — конвертация в .mrs формат
- [sing-box](https://github.com/SagerNet/sing-box) v1.12.12 — компиляция в .srs формат
- `buildtools/deduplicate.py` — ручная дедупликация доменов через DNS-резолвинг и сверку с GeoIP

## 📅 Обновления

> Файлы обновляются **при каждом пуше в master** и автоматически триггерят обновление [roscomvpn-routing](https://github.com/hydraponique/roscomvpn-routing)

## 🔗 Связанные проекты

- [roscomvpn-geoip](https://github.com/hydraponique/roscomvpn-geoip) — IP-диапазоны
- [roscomvpn-routing](https://github.com/hydraponique/roscomvpn-routing) — готовые конфиги роутинга

---

<div align="center">

> **Ставь ⭐** и не пропусти регулярные обновления для поддержания актуальности списков и оптимальной производительности

##### USDT TRC20: TMu3N2ZjK5omJ7n3WAj5MNCSM5querBXsR

##### Спасибо Всем за поддержку!
###### Сделано с ❤️ к свободному интернету!

</div>
