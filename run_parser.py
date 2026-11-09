from src.parser import ForumParser
from src.database import DatabaseRepository

parser = ForumParser()
repo = DatabaseRepository('comments.db') 

url = "https://habr.com/ru/articles/797393/comments/"

print(f"Парсим {url} ...")
comments = parser.parse_page(url)

print(f"\n Найдено комментариев: {len(comments)}\n")

for c in comments[:3]:
    print("=" * 70)
    print(f"ID:    {c['id']}")
    print(f"Автор: {c['name']}")
    print(f"HTML (первые 300 символов):")
    print(c['message'][:300])
    print()

saved = parser.save_to_db(comments, repo)
print(f"Сохранено в БД: {saved} из {len(comments)}")