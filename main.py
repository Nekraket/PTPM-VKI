import logging
import sys
import math

def process_triangle(side_a_str: str, side_b_str: str, side_c_str: str):
    logging.info(f"Получен запрос на обработку сторон: A='{side_a_str}', B='{side_b_str}', C='{side_c_str}'")

    try:
        a = float(side_a_str)
        b = float(side_b_str)
        c = float(side_c_str)
    except ValueError:
        logging.error("Ошибка: Входные данные содержат нечисловые значения.")
        logging.exception("Детали исключения ValueError:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or b == c or a == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    # Вершина A всегда в (0, 0). Вершина B на оси X: (a, 0).
    try:
        # Находим косинус угла между сторонами a и c по теореме косинусов
        cos_alpha = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        alpha = math.acos(cos_alpha)

        # Дай бог помнить... чё-то там проекция на x это длина на косинус на y длина на sin
        cx = c * math.cos(alpha)
        cy = c * math.sin(alpha)

        coordinates = [
            (0, 0),
            (int(round(a)), 0),
            (int(round(cx)), int(round(cy)))
        ]
    except Exception:
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    return triangle_type, coordinates


def main():
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("=== ЗАПУСК ПРИЛОЖЕНИЯ ===")

    process_triangle("50", "50", "50")
    print("-" * 60)

    process_triangle("120", "120", "120")
    print("-" * 60)

    process_triangle("50", "-5", "50")
    print("-" * 60)

    process_triangle("10", "10", "100")
    print("-" * 60)

    process_triangle("очень-очень_хочу_спать", "50", "50")

    logging.info("=== РАБОТА ЗАВЕРШЕНА ===")


if __name__ == "__main__":
    main()




# import logging
#
# try:
#     a = 10
#     for b in range(0, 3):
#         logging.info(f"Итерация b = {b}")
#
#         if b == 0:
#             logging.warning("Внимание, переменная b инициализирована нулем!")
#
#         logging.debug(f"Выполнение деления {a} на {b}")
#         result = a / b
#         logging.info(f"Деление {a} на {b} равно {result}")
#
# except ZeroDivisionError as ex:
#     # Метод logging.exception() автоматически прикрепляет traceback (стек ошибки)
#     logging.error("Что-то пошло не так...")
#     logging.exception("Заход в блок обработки исключения:")






# import logging
# import sys
#
# # Шаблон строки лога (аналог template в Serilog)
# # Содержит: время, уровень (до 7 символов для выравнивания), имя логгера и сообщение
# log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
# date_format = "%Y-%m-%d %H:%M:%S"
#
# # Базовая настройка корневого логгера
# logging.basicConfig(
#     level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
#     format=log_format,
#     datefmt=date_format,
#     handlers=[
#         logging.StreamHandler(sys.stdout),          # Настройка логирования в консоль
#         logging.FileHandler("Logs/file_txt.log", encoding="utf-8") # Настройка логирования в файл
#     ]
# )
#
# logging.info("Логгер успешно сконфигурирован")
# logging.info("Приложение запущено")
#
# root_logger = logging.getLogger()
#
#
# # 3. Извлекаем уровень логирования (выведет 20, так как INFO = 20)
# print("Уровень:", root_logger.level)
#
# # 4. Проверяем, что список обработчиков не пустой
# if root_logger.handlers:
#     # Берем самый первый обработчик из списка (под индексом 0)
#     first_handler = root_logger.handlers[0]
#
#     # Берем объект форматирования у этого обработчика
#     formatter = first_handler.formatter
#
#     # Выводим строку формата
#     print("Формат текста:", formatter._fmt)
# else:
#     print("Список handlers пуст")