"""Отрисовка регистров и подсветки на холсте."""


class Renderer:
    """Рисует кружки-регистры и управляет их цветом."""

    COLOR_BG = "#ffffff"
    COLOR_STRIP = "#f1ccd7"
    COLOR_CIRCLE = "#111111"
    COLOR_DIGIT = "#ffffff"
    COLOR_WEIGHT = "#666666"

    HIGHLIGHT_COLORS = [
        "#ffcc00", "#ff8800", "#ff5555", "#ff44aa",
        "#aa55ff", "#5588ff", "#44ddff", "#44ffaa",
    ]

    def __init__(self, canvas, model):
        """Сохранить холст и модель, задать размеры регистров."""
        self.canvas = canvas
        self.model = model
        self.radius = 24
        self.spacing = 62
        self.origin_x = 30
        self.origin_y = 75
        self.circle_ids = []
        self.text_ids = []
        self.weight_ids = []

    def draw_all(self):
        """Полностью перерисовать холст."""
        self.canvas.delete("all")
        self._draw_strip()
        self._draw_registers()

    def _draw_strip(self):
        """Нарисовать фоновую плашку под регистрами."""
        total_w = (self.origin_x * 2
                   + (self.model.size - 1) * self.spacing
                   + self.radius * 2)
        height = self.origin_y + self.radius + 30
        self.canvas.create_rectangle(0, 0, total_w, height,
                                     fill=self.COLOR_STRIP, outline="")

    def _draw_registers(self):
        """Нарисовать кружки с цифрами и весами."""
        self.circle_ids.clear()
        self.text_ids.clear()
        self.weight_ids.clear()
        weights = self.model.current_weights()
        for i, digit in enumerate(self.model.digits):
            x, y = self._center(i)
            r = self.radius
            circle_id = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.COLOR_CIRCLE, outline=""
            )
            text_id = self.canvas.create_text(
                x, y, text=str(digit), fill=self.COLOR_DIGIT,
                font=("Segoe UI", 16, "bold")
            )
            weight_id = self.canvas.create_text(
                x, y + r + 16, text=f"×{weights[i]}",
                fill=self.COLOR_WEIGHT, font=("Segoe UI", 10)
            )
            self.circle_ids.append(circle_id)
            self.text_ids.append(text_id)
            self.weight_ids.append(weight_id)

    def _center(self, index):
        """Вернуть координаты центра регистра по его индексу."""
        x = self.origin_x + self.radius + index * self.spacing
        y = self.origin_y
        return x, y

    def get_register_center(self, index):
        """Публичный доступ к координатам центра регистра."""
        return self._center(index)

    def highlight_register(self, index, color):
        """Подсветить регистр указанным цветом."""
        if 0 <= index < len(self.circle_ids):
            self.canvas.itemconfigure(self.circle_ids[index], fill=color)

    def reset_register_color(self, index):
        """Вернуть регистру его обычный цвет."""
        if 0 <= index < len(self.circle_ids):
            self.canvas.itemconfigure(self.circle_ids[index],
                                      fill=self.COLOR_CIRCLE)
