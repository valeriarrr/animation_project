"""Математическая модель регистров и систем счисления."""

import math


class NumberModel:
    """Хранит цифры регистров и считает значение в разных системах."""

    def __init__(self, size=8):
        """Создать модель с заданным числом регистров."""
        self.size = size
        self.current_system = "binary"
        self.digits = [0] * size

    def allowed_values(self, index):
        """Вернуть список цифр, допустимых в регистре index."""
        if self.current_system == "binary":
            return [0, 1]
        if self.current_system == "balanced_ternary":
            return [-1, 0, 1]
        if self.current_system == "mixed":
            weight = self.weights_mixed()[index]
            return list(range(0, weight + 1))
        return [0]

    def next_value(self, index):
        """Переключить цифру регистра на следующую по кругу."""
        values = self.allowed_values(index)
        current = self.digits[index]
        if current not in values:
            self.digits[index] = values[0]
            return
        position = values.index(current)
        self.digits[index] = values[(position + 1) % len(values)]

    def reset(self):
        """Сбросить все регистры в ноль."""
        self.digits = [0] * self.size

    def set_system(self, system):
        """Сменить систему счисления и обнулить регистры."""
        self.current_system = system
        self.digits = [0] * self.size

    def weights_binary(self):
        """Вернуть веса разрядов для двоичной системы."""
        return [2 ** (self.size - 1 - i) for i in range(self.size)]

    def weights_balanced_ternary(self):
        """Вернуть веса разрядов для троичной уравновешенной."""
        return [3 ** (self.size - 1 - i) for i in range(self.size)]

    def weights_mixed(self):
        """Вернуть веса разрядов для смешанной системы."""
        return [math.factorial(self.size - 1 - i)
                for i in range(self.size)]

    def current_weights(self):
        """Вернуть веса разрядов для текущей системы счисления."""
        if self.current_system == "binary":
            return self.weights_binary()
        if self.current_system == "balanced_ternary":
            return self.weights_balanced_ternary()
        return self.weights_mixed()

    def value(self):
        """Посчитать итоговое значение по текущим цифрам и весам."""
        weights = self.current_weights()
        return sum(d * w for d, w in zip(self.digits, weights))

    def system_title(self):
        """Вернуть человекочитаемое название текущей системы."""
        return {
            "binary": "Двоичная",
            "balanced_ternary": "Троичная уравновешенная",
            "mixed": "Смешанное основание",
        }.get(self.current_system, self.current_system)
