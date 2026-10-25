import logging
import sys
import os

from src.calculations import Calculator
from src.database import Database
from src.user_interface import ConsoleUserInterface
from src.notifier import EmailNotifier
from src.controller import Controller

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(name)-12s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "triangles.db")

def main():
    logger = logging.getLogger("main")
    logger.info("=== ЗАПУСК ПРИЛОЖЕНИЯ ===")
    logger.info(f"Файл БД: {DB_PATH}")

    calculator = Calculator()
    database = Database(DB_PATH)
    ui = ConsoleUserInterface()
    notifier = EmailNotifier()
    controller = Controller(calculator, database, ui, notifier)

    try:
        while True:
            try:
                result = controller.run_scenario()
                ui.show_message(f"[РЕЗУЛЬТАТ] {result}")
            except EOFError:
                logger.info("EOF (Ctrl+D) — выход")
                break
            except KeyboardInterrupt:
                print()
                logger.info("Ctrl+C — выход")
                break

            answer = ui.get_input("Продолжить? (y/n): ").strip().lower()
            if answer != "y":
                break
    finally:
        database.close()
        logger.info("=== РАБОТА ЗАВЕРШЕНА ===")


if __name__ == "__main__":
    main()