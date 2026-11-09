import os
import requests

url = "https://habr.com/ru/articles/797393/comments/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get(url, headers=headers, timeout=10)
r.raise_for_status()
print(f"Статус: {r.status_code}, длина: {len(r.text)} символов")

os.makedirs('tests/fixtures', exist_ok=True)
path = 'tests/fixtures/habr_fixture.html'

with open(path, 'w', encoding='utf-8') as f:
    f.write(r.text)

print(f"Сохранено в {path}")