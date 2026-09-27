import unittest
from src.delivery_service import calculate_delivery_cost

class TestDeliveryValidation(unittest.TestCase):
    def test_weight_below_minimum_returns_error(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_exactly_maximum_is_valid(self):
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)
        self.assertNotEqual(date, "0000-00-00")

    def test_weight_exactly_minimum_is_valid(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_zero_returns_error(self):
        cost, date = calculate_delivery_cost(10, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(10, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_exactly_maximum_is_valid(self):
        cost, date = calculate_delivery_cost(10, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_exactly_minimum_is_valid(self):
        cost, date = calculate_delivery_cost(10, 1, "обычный")
        self.assertNotEqual(cost, -1)

    def test_invalid_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(10, 100, "секретный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_empty_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(10, 100, "")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")


class TestDeliveryInvalidType(unittest.TestCase):
    def test_string_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_delivery_cost("10", 100, "обычный")
    def test_string_distance_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_delivery_cost(10, "100", "обычный")
    def test_none_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_delivery_cost(None, 100, "обычный")


class TestDeliveryBaseCost(unittest.TestCase):
    def test_base_cost_for_light_package(self):
        """Вес 1 кг, 100 км, обычный: 200 + 100*5 = 700."""
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_base_cost_for_minimum_distance(self):
        """Вес 1 кг, 1 км: 200 + 5 = 205."""
        cost, _ = calculate_delivery_cost(1, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_base_cost_for_maximum_distance(self):
        """Вес 1 кг, 5000 км: 200 + 25000 = 25200."""
        cost, _ = calculate_delivery_cost(1, 5000, "обычный")
        self.assertEqual(cost, 25200)


class TestDeliveryWeightCoefficients(unittest.TestCase):
    def test_weight_exactly_5_no_coefficient(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        # 200 + 500 = 700, без множителя
        self.assertEqual(cost, 700)

    def test_weight_just_above_5_applies_1_2(self):
        """Вес 5.1 — множитель 1.2."""
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        # (200 + 500) * 1.2 = 840
        self.assertEqual(cost, 840)

    def test_weight_just_below_20_applies_1_2(self):
        """Вес 19.9 — множитель 1.2."""
        cost, _ = calculate_delivery_cost(19.9, 100, "обычный")
        # 700 * 1.2 = 840
        self.assertEqual(cost, 840)

    def test_weight_exactly_20_applies_1_5(self):
        """Вес ровно 20.0 — множитель 1.5 (граница >= 20.0)."""
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        # 700 * 1.5 = 1050
        self.assertEqual(cost, 1050)

    def test_weight_50_applies_1_5(self):
        """Вес 50.0 (максимум) — множитель 1.5."""
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        # 700 * 1.5 = 1050
        self.assertEqual(cost, 1050)


class TestDeliveryPackageTypeSurcharge(unittest.TestCase):
    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        # 700 + 300 = 1000
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        # 700 + 1000 = 1700
        self.assertEqual(cost, 1700)

    def test_regular_no_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_fragile_surcharge_applies_after_weight_coefficient(self):
        cost, _ = calculate_delivery_cost(20, 100, "хрупкий")
        # 700 * 1.5 = 1050; 1050 + 300 = 1350
        self.assertEqual(cost, 1350)

    def test_dangerous_surcharge_applies_after_weight_coefficient(self):
        cost, _ = calculate_delivery_cost(20, 100, "опасный")
        # 700 * 1.5 = 1050; 1050 + 1000 = 2050
        self.assertEqual(cost, 2050)


class TestDeliveryExpressDiscount(unittest.TestCase):
    def test_express_halves_cost(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        # 700 * 0.5 = 350
        self.assertEqual(cost, 350)

    def test_express_with_fragile(self):
        """Экспресс + хрупкая."""
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий", is_express=True)
        # (700 + 300) * 0.5 = 500.
        self.assertEqual(cost, 500)

    def test_express_with_dangerous(self):
        """Экспресс + опасная."""
        cost, _ = calculate_delivery_cost(1, 100, "опасный", is_express=True)
        # (700 + 1000) * 0.5 = 850
        self.assertEqual(cost, 850)


class TestDeliveryDateCalculation(unittest.TestCase):
    def test_minimum_distance_one_day(self):
        _, date = calculate_delivery_cost(1, 1, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_500_one_day(self):
        _, date = calculate_delivery_cost(1, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_1000_two_days(self):
        _, date = calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_distance_1500_three_days(self):
        _, date = calculate_delivery_cost(1, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")


class TestDeliveryExpressDate(unittest.TestCase):
    def test_express_one_day_becomes_zero(self):
        _, date = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        # distance=100 -> days_needed = max(1, 0) = 1 -> 1 // 2 = 0
        self.assertEqual(date, "2026-09-03")

    def test_express_two_days_becomes_one(self):
        _, date = calculate_delivery_cost(1, 1000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")


class TestDeliveryReturnTypes(unittest.TestCase):
    def test_cost_is_integer(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertIsInstance(cost, int)

    def test_date_is_string(self):
        _, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertIsInstance(date, str)

    def test_date_format_is_iso(self):
        """Дата в формате YYYY-MM-DD."""
        _, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()