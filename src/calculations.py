import logging
import math

logger = logging.getLogger(__name__)

class Calculator:
    def process_triangle(self, side_a_str: str, side_b_str: str, side_c_str: str):
        logger.info(f"Обработка сторон: A={side_a_str}, B={side_b_str}, C={side_c_str}")

        try:
            a = float(side_a_str)
            b = float(side_b_str)
            c = float(side_c_str)
        except ValueError:
            logger.error("Нечисловые данные")
            return "", [(-2, -2), (-2, -2), (-2, -2)]

        if a <= 0 or b <= 0 or c <= 0:
            logger.error("Стороны должны быть > 0")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            logger.warning(f"Предупреждение: Стороны {a}, {b}, {c} не могут образовать треугольник.")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a == b == c:
            triangle_type = "равносторонний"
        elif a == b or b == c or a == c:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

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
        except Exception:
            logger.exception("Ошибка расчёта координат")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        return triangle_type, coordinates