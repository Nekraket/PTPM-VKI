import unittest
from src.delivery_service import calculate_delivery_cost


class TestDeliveryService(unittest.TestCase):

    # --- Валидация параметров ---

    def test_weight_below_min_return_error(self):
        cost, date = calculate_delivery_cost(0.09, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_max_return_error(self):
        cost, _ = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_zero_distance_return_error(self):
        cost, _ = calculate_delivery_cost(10.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_max_return_error(self):
        cost, _ = calculate_delivery_cost(10.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type_return_error(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "коробка")
        self.assertEqual(cost, -1)

    # --- Весовые коэффициенты ---

    def test_light_weight_has_no_coefficient(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_has_coefficient_1_2(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_has_coefficient_1_5(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    # --- Надбавки за тип упаковки ---

    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    # --- Экспресс-доставка (баги) ---

    def test_express_adds_surcharge_not_discount(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_express_short_distance_keeps_min_one_day(self):
        _, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_express_combines_with_heavy_and_dangerous(self):
        # (200 + 100*5)*1.5 + 1000 = 1800 + 1000 = 2800, экспресс ×0.5 → 1400 (ожидаем наценку)
        cost, _ = calculate_delivery_cost(30.0, 100, "опасный", is_express=True)
        self.assertEqual(cost, 1400)

    # --- Округление дней ---

    def test_intermediate_distance_rounds_days_up(self):
        _, date = calculate_delivery_cost(2.0, 501, "обычный")
        self.assertEqual(date, "2026-09-05")

    # --- Границы веса ---

    def test_weight_exact_min_boundary(self):
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_exact_max_boundary(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_exact_5kg_has_no_coefficient(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    # --- Даты обычной доставки ---

    def test_distance_500_is_one_day(self):
        _, date = calculate_delivery_cost(2.0, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_1000_is_two_days(self):
        _, date = calculate_delivery_cost(2.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_max_distance_is_ten_days(self):
        _, date = calculate_delivery_cost(2.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    # --- Комбинированные тарифы ---

    def test_heavy_dangerous_combines_tariffs(self):
        cost, _ = calculate_delivery_cost(30.0, 200, "опасный")
        self.assertEqual(cost, 2800)

if __name__ == "__main__":
    unittest.main()