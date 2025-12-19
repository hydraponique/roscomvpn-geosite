import urllib.request
from urllib.parse import urlparse

# Основные доменные зоны
target_zones = {'ru', 'su', 'xn--p1ai', 'moscow', 'volga', 'tatar', 'yandex', 
                'xn--d1acj3b', 'xn--80asehdb', 'xn--c1avg', 'xn--80aswg', 
                'xn--80adxhks', 'by', 'xn--90ais', 'kz', 'xn--80ao21a'}

# Двухуровневые доменные зоны (особые случаи)
two_level_zones = {
    'ru.net', 'org.ru', 'net.ru', 'com.kz', 'org.kz', 'com.ru', 'spb.ru', 'msk.ru',
    'moy.su', 'ucoz.ru', 'narod.ru', '3dn.ru', 'my1.ru', 'okis.ru', 'had.su',
    'clan.su', 'wix.ru', 'listbb.ru', 'allbest.ru', 'mya5.ru', 'liveforums.ru',
    'forum24.ru', 'appbu.ru'
}

# Список источников
source_urls = [
    "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/refs/heads/main/domains_all.lst",
    "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/refs/heads/main/ooni_domains.lst",
    "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/refs/heads/main/community.lst",
    "https://community.antifilter.download/list/domains.lst"
]

filtered_minimized = []

for source_url in source_urls:
    try:
        with urllib.request.urlopen(source_url) as response:
            content = response.read().decode('utf-8').splitlines()
            
            for line in content:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                domain = line
                
                # Сначала проверяем двухуровневые зоны
                for zone in two_level_zones:
                    if domain.endswith('.' + zone):
                        # Разделяем домен по точкам
                        parts = domain.split('.')
                        # Находим индекс начала двухуровневой зоны
                        for i in range(len(parts) - 1):
                            if '.'.join(parts[i:i+2]) == zone:
                                # Берем предшествующую часть + всю двухуровневую зону
                                minimized = '.'.join(parts[max(0, i-1):]) if i > 0 else domain
                                filtered_minimized.append(minimized)
                                break
                        else:
                            filtered_minimized.append(domain)
                        break
                else:
                    # Проверяем обычные одноуровневые зоны
                    for zone in target_zones:
                        if domain.endswith('.' + zone):
                            # Разделяем домен по точкам
                            parts = domain.split('.')
                            # Находим индекс зоны
                            if parts[-1] == zone:
                                # Берем предшествующую часть + зону
                                minimized = '.'.join(parts[-2:]) if len(parts) >= 2 else domain
                                filtered_minimized.append(minimized)
                            break
    except Exception:
        continue

# Удаляем дубликаты и сохраняем
with open('data/category-rkn', 'w', encoding='utf-8') as f:
    for domain in sorted(set(filtered_minimized)):
        f.write(domain + '\n')