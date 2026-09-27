import unittest
from src.my_project import process_triangle

class TestProcessTriangleType(unittest.TestCase):
    def test_equilateral_triangle_type(self):
        triangle_type, _ = process_triangle("50", "50", "50")
        self.assertEqual(triangle_type, "равносторонний")

    def test_isosceles_triangle_type_ab_equal(self):
        triangle_type, _ = process_triangle("10", "10", "12")
        self.assertEqual(triangle_type, "равнобедренный")
    def test_isosceles_triangle_type_bc_equal(self):
        triangle_type, _ = process_triangle("12", "10", "10")
        self.assertEqual(triangle_type, "равнобедренный")
    def test_isosceles_triangle_type_ac_equal(self):
        triangle_type, _ = process_triangle("10", "12", "10")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_scalene_triangle_type(self):
        triangle_type, _ = process_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")


class TestProcessTriangleInvalidInput(unittest.TestCase):
    def test_non_numeric_input_returns_empty_type(self):
        triangle_type, coords = process_triangle("abc", "50", "50")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])
    def test_non_numeric_second_argument(self):
        triangle_type, coords = process_triangle("50", "xyz", "50")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])
    def test_non_numeric_third_argument(self):
        triangle_type, coords = process_triangle("50", "50", "!")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_zero_side_is_not_triangle(self):
        triangle_type, coords = process_triangle("0", "50", "50")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_is_not_triangle(self):
        triangle_type, coords = process_triangle("50", "-5", "50")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_inequality_violation_returns_not_triangle(self):
        triangle_type, coords = process_triangle("10", "10", "100")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_degenerate_triangle_sum_equals_third(self):
        triangle_type, _ = process_triangle("5", "5", "10")
        self.assertEqual(triangle_type, "не треугольник")

    def test_float_strings_accepted(self):
        triangle_type, _ = process_triangle("3.5", "4.5", "5.5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_coordinates_are_int(self):
        _, coords = process_triangle("3", "4", "5")
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

if __name__ == "__main__":
    unittest.main()