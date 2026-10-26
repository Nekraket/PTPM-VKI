import unittest
from src.Converter import Converter

class TestUpperRange(unittest.TestCase):

    def test_left_boundary_included(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_just_above_boundary(self):
        self.assertEqual(Converter.do(100.8), 1000)

    def test_far_above(self):
        self.assertEqual(Converter.do(999.9), 1000)


class TestPositiveRange(unittest.TestCase):

    def test_smallest_positive(self):
        self.assertEqual(Converter.do(0.1), 0)

    def test_less_than_one(self):
        self.assertEqual(Converter.do(0.9), 0)

    def test_whole_number(self):
        self.assertEqual(Converter.do(5.0), 5)

    def test_fraction_truncated(self):
        self.assertEqual(Converter.do(5.9), 5)
        self.assertEqual(Converter.do(99.9), 99)


class TestZero(unittest.TestCase):

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)


class TestNegativeSmallRange(unittest.TestCase):

    def test_just_below_zero(self):
        self.assertEqual(Converter.do(-0.1), -5)

    def test_minus_half(self):
        self.assertEqual(Converter.do(-0.5), -5)

    def test_minus_one(self):
        self.assertEqual(Converter.do(-1.0), -6)

    def test_middle_value(self):
        self.assertEqual(Converter.do(-15.7), -20)

    def test_left_boundary_included(self):
        self.assertEqual(Converter.do(-30.4), -35)


class TestLowerRange(unittest.TestCase):

    def test_right_boundary_included(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_just_below_boundary(self):
        self.assertEqual(Converter.do(-30.6), -2000)

    def test_far_below(self):
        self.assertEqual(Converter.do(-100.0), -2000)
        self.assertEqual(Converter.do(-99999.9), -2000)

if __name__ == "__main__":
    unittest.main()