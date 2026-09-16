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
        logging.error(f"Ошибка: Длины сторон должны быть строго больше нуля! (Передано: A={a}, B={b}, C={c})")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        logging.warning(f"Предупреждение: Стороны {a}, {b}, {c} не могут образовать треугольник.")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or b == c or a == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logging.info(f"Успешно определен тип фигуры: {triangle_type}")

    try:
        cos_alpha = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        alpha = math.acos(cos_alpha)

        cx = c * math.cos(alpha)
        cy = c * math.sin(alpha)

        coordinates = [
            (0, 0),
            (int(round(a)), 0),
            (int(round(cx)), int(round(cy)))
        ]

        if int(round(a)) > 100 or int(round(cx)) > 100 or int(round(cy)) > 100:
            logging.warning(f"Внимание: Фигура выходит за рамки поля 100x100 px! Координаты: {coordinates}")
        else:
            logging.info(f"Успешно рассчитаны координаты в поле: {coordinates}")

    except Exception:
        logging.error("Произошла непредвиденная математическая ошибка при расчете координат.")
        logging.exception("Трассировка ошибки расчетов:")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    logging.info(f"ИТОГ ЗАПРОСА => Тип: {triangle_type}, Координаты: {coordinates}")
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



# root_logger = logging.getLogger()

# if root_logger.handlers:
#     first_handler = root_logger.handlers[0]
#
#     formatter = first_handler.formatter
#
#     print("Формат текста:", formatter._fmt)
# else:
#     print("Список handlers пуст")