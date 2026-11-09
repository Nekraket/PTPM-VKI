import requests
from bs4 import BeautifulSoup


class ForumParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        }

    def parse_page(self, url: str):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            return []

        return self._parse_html(response.text)

    def _parse_html(self, html_content: str):
        soup = BeautifulSoup(html_content, 'lxml')
        comments = []

        comment_blocks = soup.find_all('article', class_='tm-comment-thread__comment')

        for block in comment_blocks:
            raw_id = block.get('id', '')

            if not raw_id.isdigit():
                continue

            comment_id = int(raw_id)

            author_tag = block.find('a', class_='tm-user-info__username')
            author_name = author_tag.get_text(strip=True) if author_tag else "Unknown"

            body_container = block.find('div', class_='tm-comment__body-content')

            if body_container:
                message_html = body_container.decode_contents()
            else:
                message_html = ""

            comments.append({
                'id': comment_id,
                'name': author_name,
                'message': message_html
            })

        return comments

    def save_to_db(self, parsed_data: list, repository):
        saved_count = 0
        for comment in parsed_data:
            try:
                repository.add(comment['id'], comment['name'], comment['message'])
                saved_count += 1
            except Exception as e:
                print(f"Не удалось сохранить комментарий {comment['id']}: {e}")
        return saved_count