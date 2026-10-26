class Converter:

    @staticmethod
    def do(x: float) -> int:
        if x >= 100.7:
            return 1000

        if x > 0:
            return int(x)

        if x == 0.0:
            raise ValueError("x не может быть равен 0.0")

        if x >= -30.4:
            return int(x) - 5

        return -2000