import sqlite3
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT,
                side_b TEXT,
                side_c TEXT,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.connection.commit()

    def add_record(self, side_a: str, side_b: str, side_c: str, triangle_type: str, error_message: str = ""):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (side_a, side_b, side_c, triangle_type, error_message))
        self.connection.commit()
        logger.info(f"Запись добавлена: {side_a},{side_b},{side_c} -> {triangle_type}")

    def get_record(self, side_a: str, side_b: str, side_c: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT triangle_type, error_message FROM triangles
            WHERE side_a=? AND side_b=? AND side_c=?
        """, (side_a, side_b, side_c))
        return cursor.fetchone()

    def delete_record(self, side_a: str, side_b: str, side_c: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            DELETE FROM triangles
            WHERE side_a=? AND side_b=? AND side_c=?
        """, (side_a, side_b, side_c))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()