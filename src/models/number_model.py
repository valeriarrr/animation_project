# Здесь вся математика: хранение битов, перевод в разные системы счисления
import math


class NumberModel:
    def __init__(self, size=8):
        self.size = size
        self.current_system = "binary"
        self.digits = [0] * size

    def allowed_values(self, index):
        # какие цифры допустимы в регистре
        if self.current_system == "binary":
            return [0, 1]
        if self.current_system == "balanced_ternary":
            return [-1, 0, 1]
        if self.current_system == "mixed":
            w = self.weights_mixed()[index]
            return list(range(0, w + 1))
        return [0]

    def next_value(self, index):
        # клик: увеличить цифру, с максимума — на минимум
        values = self.allowed_values(index)
        cur = self.digits[index]
        if cur not in values:
            self.digits[index] = values[0]
            return
        pos = values.index(cur)
        self.digits[index] = values[(pos + 1) % len(values)]

    def reset(self):
        self.digits = [0] * self.size

    def set_system(self, system):
        self.current_system = system
        self.digits = [0] * self.size

    def weights_binary(self):
        return [2 ** (self.size - 1 - i) for i in range(self.size)]

    def weights_balanced_ternary(self):
        return [3 ** (self.size - 1 - i) for i in range(self.size)]

    def weights_mixed(self):
        return [math.factorial(self.size - 1 - i) for i in range(self.size)]

    def current_weights(self):
        if self.current_system == "binary":
            return self.weights_binary()
        if self.current_system == "balanced_ternary":
            return self.weights_balanced_ternary()
        return self.weights_mixed()

    def value(self):
        weights = self.current_weights()
        return sum(d * w for d, w in zip(self.digits, weights))

    def system_title(self):
        return {
            "binary": "Двоичная",
            "balanced_ternary": "Троичная уравновешенная",
            "mixed": "Смешанное основание",
        }.get(self.current_system, self.current_system)
