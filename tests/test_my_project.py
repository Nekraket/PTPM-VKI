import unittest
from src.my_project import process_triangle


class TestMyProjectTriangle(unittest.TestCase):

    # --- Нечисловые входные данные ---

    def test_letters_in_side_return_error_coords(self):
        result_type, coords = process_triangle("abc", "50", "50")
        self.assertEqual(result_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_string_in_side_return_error_coords(self):
        result_type, coords = process_triangle("", "50", "50")
        self.assertEqual(result_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_special_chars_in_side_return_error_coords(self):
        result_type, coords = process_triangle("50#", "50", "50")
        self.assertEqual(result_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # --- Неположительные стороны ---

    def test_zero_side_return_not_a_triangle(self):
        result_type, coords = process_triangle("0", "50", "50")
        self.assertEqual(result_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_return_not_a_triangle(self):
        result_type, coords = process_triangle("50", "-10", "50")
        self.assertEqual(result_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_all_zero_sides_return_not_a_triangle(self):
        result_type, _ = process_triangle("0", "0", "0")
        self.assertEqual(result_type, "не треугольник")

    # --- Неравенство треугольника ---

    def test_sum_equals_third_side_return_not_a_triangle(self):
        result_type, coords = process_triangle("10", "20", "30")
        self.assertEqual(result_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_sum_less_than_third_side_return_not_a_triangle(self):
        result_type, _ = process_triangle("10", "10", "50")
        self.assertEqual(result_type, "не треугольник")

    # --- Типы треугольников ---

    def test_equal_sides_return_equilateral(self):
        result_type, _ = process_triangle("50", "50", "50")
        self.assertEqual(result_type, "равносторонний")

    def test_a_equals_b_return_isosceles(self):
        result_type, _ = process_triangle("50", "50", "30")
        self.assertEqual(result_type, "равнобедренный")

    def test_b_equals_c_return_isosceles(self):
        result_type, _ = process_triangle("30", "50", "50")
        self.assertEqual(result_type, "равнобедренный")

    def test_all_sides_different_return_versatile(self):
        result_type, _ = process_triangle("3", "4", "5")
        self.assertEqual(result_type, "разносторонний")

    # --- Правильность вычисления координаты ---

    def test_equilateral_coords_are_correct(self):
        _, coords = process_triangle("50", "50", "50")
        self.assertEqual(coords, [(0, 0), (50, 0), (25, 43)])

    def test_right_triangle_coords_are_correct(self):
        _, coords = process_triangle("30", "50", "40")
        self.assertEqual(coords, [(0, 0), (30, 0), (0, 40)])

    # --- Границы поля 100x100 ---

    def test_side_100_fits_field_bounds(self):
        result_type, coords = process_triangle("100", "100", "100")
        self.assertEqual(result_type, "равносторонний")
        for x, y in coords:
            self.assertTrue(x <= 100 and y <= 100)

    def test_side_120_exceeds_field_but_returns_coords(self):
        result_type, coords = process_triangle("120", "120", "120")
        self.assertEqual(result_type, "равносторонний")
        self.assertEqual(coords[1], (120, 0))

    # --- Дробные и форматированные строки ---

    def test_float_strings_are_rounded_in_coords(self):
        result_type, coords = process_triangle("50.4", "50.4", "50.4")
        self.assertEqual(result_type, "равносторонний")
        self.assertEqual(coords[1], (50, 0))

    def test_spaces_around_numbers_are_ignored(self):
        result_type, coords = process_triangle("  50  ", "50", "50")
        self.assertEqual(result_type, "равносторонний")
        self.assertEqual(coords[1], (50, 0))

    # --- Экстремальные значения ---

    def test_very_large_sides_are_processed(self):
        result_type, _ = process_triangle("1e21", "1e21", "1e21")
        self.assertEqual(result_type, "равносторонний")

    def test_tiny_side_near_zero_is_valid(self):
        result_type, _ = process_triangle("0.000001", "50", "50")
        self.assertEqual(result_type, "равнобедренный")


if __name__ == "__main__":
    unittest.main()