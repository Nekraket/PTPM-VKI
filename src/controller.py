import logging

logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, calculator, database, ui, notifier):
        self.calculator = calculator
        self.database = database
        self.ui = ui
        self.notifier = notifier

    def run_scenario(self):
        side_a = self.ui.get_input("Сторона A: ")
        side_b = self.ui.get_input("Сторона B: ")
        side_c = self.ui.get_input("Сторона C: ")

        logger.info(f"Введены стороны: {side_a}, {side_b}, {side_c}")

        record = self.database.get_record(side_a, side_b, side_c)

        if record:
            triangle_type, error_message = record
            logger.info(f"Результат взят из БД: {triangle_type}")
        else:
            triangle_type, _ = self.calculator.process_triangle(side_a, side_b, side_c)
            if triangle_type == "":
                error_message = "Нечисловые данные"
            elif triangle_type == "не треугольник":
                error_message = "Не треугольник"
            else:
                error_message = ""
            self.database.add_record(side_a, side_b, side_c, triangle_type, error_message)
            logger.info(f"Результат вычислен и сохранён: {triangle_type}")

        result_message = f"Треугольник {side_a},{side_b},{side_c}: {triangle_type}"
        self.notifier.send(result_message)

        self.ui.show_message(result_message)
        return triangle_type