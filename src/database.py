import sqlite3

class DatabaseError(Exception):
    pass

class ValidationError(DatabaseError):
    pass

class DuplicateError(DatabaseError):
    pass


class DatabaseRepository:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def _validate_data(self, username: str, message: str):
        if not isinstance(username, str) or not isinstance(message, str):
            raise ValidationError("Имя и сообщение должны быть строками.")

        if len(username) > 256:
            raise ValidationError("Имя пользователя не должно превышать 256 символов.")

        if len(message) > 8096:
            raise ValidationError("Сообщение не должно превышать 8096 символов.")


    def get_by_id(self, comment_id: int):
        self.cursor.execute("SELECT id, name, message FROM comments WHERE id = ?", (comment_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_by_name(self, username: str):
        self.cursor.execute("SELECT id, name, message FROM comments WHERE name = ?", (username,))
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def add(self, comment_id: int, username: str, message: str):
        self._validate_data(username, message)

        if not isinstance(comment_id, int):
            raise ValidationError("ID должен быть целым числом.")

        try:
            self.cursor.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise DuplicateError(f"Комментарий с ID {comment_id} уже существует.")

    def update(self, comment_id: int, new_message: str):
        if not isinstance(new_message, str):
            raise ValidationError("Сообщение должно быть строкой.")

        if len(new_message) > 8096:
            raise ValidationError("Сообщение не должно превышать 8096 символов.")

        self.cursor.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id)
        )
        self.conn.commit()

        return self.cursor.rowcount > 0

    def delete(self, comment_id: int):
        self.cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0