class Renderer:
    COLOR_BG = "#ffffff"
    COLOR_STRIP = "#e8e8e8"
    COLOR_CIRCLE = "#111111"
    COLOR_DIGIT = "#ffffff"
    COLOR_WEIGHT = "#666666"

    HIGHLIGHT_COLORS = [
        "#ffcc00", "#ff8800", "#ff5555", "#ff44aa",
        "#aa55ff", "#5588ff", "#44ddff", "#44ffaa",
    ]

    def __init__(self, canvas, model):
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
        self.canvas.delete("all")
        self._draw_strip()
        self._draw_registers()

    def _draw_strip(self):
        total_w = (self.origin_x * 2
                   + (self.model.size - 1) * self.spacing
                   + self.radius * 2)
        h = self.origin_y + self.radius + 30
        self.canvas.create_rectangle(0, 0, total_w, h,
                                     fill=self.COLOR_STRIP, outline="")

    def _draw_registers(self):
        self.circle_ids.clear()
        self.text_ids.clear()
        self.weight_ids.clear()
        weights = self.model.current_weights()
        for i, digit in enumerate(self.model.digits):
            x, y = self._center(i)
            r = self.radius
            cid = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.COLOR_CIRCLE, outline=""
            )
            tid = self.canvas.create_text(
                x, y, text=str(digit), fill=self.COLOR_DIGIT,
                font=("Segoe UI", 16, "bold")
            )
            wid = self.canvas.create_text(
                x, y + r + 16, text=f"×{weights[i]}",
                fill=self.COLOR_WEIGHT, font=("Segoe UI", 10)
            )
            self.circle_ids.append(cid)
            self.text_ids.append(tid)
            self.weight_ids.append(wid)

    def _center(self, index):
        x = self.origin_x + self.radius + index * self.spacing
        y = self.origin_y
        return x, y

    def get_register_center(self, index):
        return self._center(index)

    def highlight_register(self, index, color):
        if 0 <= index < len(self.circle_ids):
            self.canvas.itemconfigure(self.circle_ids[index], fill=color)

    def reset_register_color(self, index):
        if 0 <= index < len(self.circle_ids):
            self.canvas.itemconfigure(self.circle_ids[index],
                                      fill=self.COLOR_CIRCLE)
