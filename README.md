<div align="center">

| [RoscomVPN GeoIP](https://github.com/hydraponique/roscomvpn-geoip) | [**🌐 RoscomVPN GeoSite**](https://github.com/hydraponique/roscomvpn-geosite) | [RoscomVPN Routing](https://github.com/hydraponique/roscomvpn-routing) |
|:---:|:---:|:---:|
| ![Downloads](https://img.shields.io/github/downloads/hydraponique/roscomvpn-geoip/total.svg) ![jsDelivr](https://data.jsdelivr.com/v1/package/gh/hydraponique/roscomvpn-geoip/badge) | ![Downloads](https://img.shields.io/github/downloads/hydraponique/roscomvpn-geosite/total.svg) ![jsDelivr](https://data.jsdelivr.com/v1/package/gh/hydraponique/roscomvpn-geosite/badge) | ![Stars](https://img.shields.io/github/stars/hydraponique/roscomvpn-routing.svg) ![Happ](https://img.shields.io/badge/Happ-blue.svg) ![Mihomo](https://img.shields.io/badge/Mihomo-grey.svg) ![Incy](https://img.shields.io/badge/Incy-darkgreen.svg) |

# 🌐 RoscomVPN Geosite

**Генерирует `geosite.dat` и рулсеты для Mihomo/sing-box**
**с категоризированными списками доменов для маршрутизации трафика РФ/РБ**

</div>

---

## 📥 Форматы и скачивание

<details open>
<summary><b>geosite.dat (V2Ray/Xray)</b></summary>

| Источник | Ссылка |
|----------|--------|
| 🔗 GitHub Releases | `https://github.com/hydraponique/roscomvpn-geosite/releases/latest/download/geosite.dat` |
| ⚡ jsDelivr CDN | `https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/release/geosite.dat` |

</details>

<details>
<summary><b>🔶 Mihomo (.mrs) и 🟣 sing-box (.srs)</b></summary>

```
https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/mihomo/{категория}.mrs

https://cdn.jsdelivr.net/gh/hydraponique/roscomvpn-geosite/sing-box/{категория}.srs
```

</details>

---

## 📋 Категории

### 🇷🇺 Россия

| Категория | Описание | Назначение |
|-----------|----------|------------|
| `whitelist` | Белый список доменов | Обязательный список в любом случае, direct |
| `category-ru` | Российские домены и сервисы | Расширение для whitelist, используется для не-БС хостов, direct |
| `category-geoblock-ru` | Геоблокированный RU контент | Серверная маршрутизация РУ сервер->Зарубеж |

### 🌍 Сервисы

| Категория | Описание | Назначение |
|-----------|----------|------------|
| `apple` | Apple сервисы | В direct, фикс пуш-уведомлений |
| `google-play` | Google Play | В direct, фикс скачиваний приложений, пушей |
| `google-deepmind` | Google DeepMind / AI | Серверная маршрутизация РУ сервер->Зарубеж |
| `microsoft` | Microsoft сервисы | В direct, экономия трафика, фикс пушей |
| `github` | GitHub | Proxy, Борьба с ТСПУ и банами РКН |
| `telegram` | Telegram | Proxy, Борьба с ТСПУ и банами РКН |
| `youtube` | YouTube | Proxy, Борьба с ТСПУ и банами РКН |
| `twitch` | Twitch | Все домены twitch, если есть twitch-ads - в direct |
| `twitch-ads` | Twitch | Отключает рекламу, поднимает качество до 1080p+ - только в proxy |
| `pinterest` | Pinterest | Убираем рекламу на сервисе, direct |

### 🎮 Игры

| Категория | Описание | Назначение |
|-----------|----------|------------|
| `steam` | Steam | В direct, экономия трафика, снижение пинга |
| `epic-games` | Epic Games Store | В direct, экономия трафика, снижение пинга |
| `riot` | Riot Games (LoL, Valorant) | В direct, экономия трафика, снижение пинга |
| `escapefromtarkov` | Escape from Tarkov | В direct, нужен для входа в любой гео-аккаунт в игре |
| `faceit` | FaceIT | В direct, расширяет список доступных серверов сервиса |
| `origin` | EA Origin | В direct, экономия трафика, снижение пинга |

### ⚙️ Прочее

| Категория | Описание | Назначение |
|-----------|----------|------------|
| `category-ads` | Рекламные домены | В block, реклама в VK/Mail.Ru |
| `win-spy` | Windows телеметрия/слежка (~377) | В block, слежка |
| `private` | Приватные/внутренние сети | Только директ, обязательный |
| `torrent` | Торрент-трекеры и DHT | Блок, работает не на 100% |

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
