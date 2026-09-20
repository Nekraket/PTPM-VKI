import logging
import sys
import math
import os

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
        logging.debug(f"[DEBUG] Вычислен cos(alpha) = {cos_alpha}")

        alpha = math.acos(cos_alpha)
        logging.debug(f"[DEBUG] Угол alpha в радианах = {alpha}")

        cx = c * math.cos(alpha)
        cy = c * math.sin(alpha)
        logging.debug(f"[DEBUG] Координаты третьей вершины (float): cx={cx}, cy={cy}")

        coordinates = [
            (0, 0),
            (int(round(a)), 0),
            (int(round(cx)), int(round(cy)))
        ]

        logging.debug(f"[DEBUG] Координаты после округления до int: {coordinates}")

        if int(round(a)) > 100 or int(round(cx)) > 100 or int(round(cy)) > 100:
            logging.warning(f"Внимание: Фигура выходит за рамки поля 100x100 px! Координаты: {coordinates}")
        else:
            logging.info(f"Успешно рассчитаны координаты в поле: {coordinates}")

    except Exception:
        logging.error("Произошла непредвиденная математическая ошибка при расчете координат.")
        logging.exception("Трассировка ошибки расчетов:")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    logging.info(f"ИТОГ ЗАПРОСА => Тип: {triangle_type}, Координаты: {coordinates}")
    print("-" * 60)
    return triangle_type, coordinates


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'Logs', 'file_txt.log')

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(file_path, encoding="utf-8")
        ]
    )

    logging.info("=== ЗАПУСК ПРИЛОЖЕНИЯ ===")

    final1 = process_triangle("50", "50", "50")
    print(final1)
    print("-" * 60)

    final2 = process_triangle("120", "120", "120")
    print(final2)
    print("-" * 60)

    final3 = process_triangle("50", "-5", "50")
    print(final3)
    print("-" * 60)

    final4 = process_triangle("10", "10", "100")
    print(final4)
    print("-" * 60)

    final5 = process_triangle("очень-очень_хочу_спать", "50", "50")
    print(final5)

    logging.info("=== РАБОТА ЗАВЕРШЕНА ===")


if __name__ == "__main__":
    main()