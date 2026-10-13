import tkinter as tk
from tkinter import font as tkfont

from src.models.number_model import NumberModel
from src.renderers.renderer import Renderer
from src.widgets.controls import SystemTabs, OvalButton


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Двоичные числа — Рошевских В.И., ПИ25-1")
        self.root.geometry("820x540")
        self.root.configure(bg="#ffffff")

        self.model = NumberModel(size=8)
        self.mode = "edit"
        self._after_ids = []
        self.change_btn = None

        self._build_ui()

    def _build_ui(self):
        # заголовок капсом, красивым шрифтом
        title_font = tkfont.Font(family="Segoe UI Semibold", size=22,
                                 weight="bold")
        tk.Label(
            self.root, text="ДВОИЧНЫЕ ЧИСЛА",
            bg="#ffffff", fg="#12406e", font=title_font
        ).pack(pady=(18, 0))

        # общий полупрозрачный овал с выбором системы
        self.tabs = SystemTabs(self.root, on_select=self._on_system_change)
        self.tabs.pack(pady=(12, 0))

        # регистры
        self.canvas = tk.Canvas(self.root, width=780, height=170,
                                bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=(10, 0))
        self.renderer = Renderer(self.canvas, self.model)
        self.renderer.draw_all()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # крупный результат
        self.result_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.result_var,
            bg="#ffffff", fg="#111111",
            font=tkfont.Font(family="Segoe UI", size=48, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=40, pady=(8, 0))

        # подпись
        self.caption_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.caption_var,
            bg="#ffffff", fg="#666666",
            font=("Segoe UI", 11), anchor="w"
        ).pack(fill="x", padx=40)

        # кнопка «Считать» — справа снизу, полупрозрачная овальная
        self.read_btn = OvalButton(
            self.root, text="Считать", command=self._on_read_click,
            width=150, height=52,
            bg="#b9d4f2", hover="#9cc3ec", text_color="#12406e",
            master_bg="#ffffff"
        )
        self.read_btn.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")

    def _on_system_change(self, system):
        self.model.set_system(system)
        self.renderer.draw_all()
        self.result_var.set("")
        self.caption_var.set("")
        self.mode = "edit"
        self._hide_change_button()

    def _on_canvas_click(self, event):
        if self.mode != "edit":
            return
        for i in range(self.model.size):
            x, y = self.renderer.get_register_center(i)
            r = self.renderer.radius
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= r * r:
                self.model.next_value(i)
                self.renderer.draw_all()
                self.result_var.set("")
                self.caption_var.set("")
                break

    def _on_read_click(self):
        if self.mode != "edit":
            return
        self.mode = "reading"
        self.result_var.set("")
        self.caption_var.set("")
        self._hide_change_button()
        self._animate_reading(0)

    def _animate_reading(self, index):
        if index >= self.model.size:
            self._finish_reading()
            return
        color = Renderer.HIGHLIGHT_COLORS[index % len(Renderer.HIGHLIGHT_COLORS)]
        self.renderer.highlight_register(index, color)

        def step():
            self.renderer.reset_register_color(index)
            self._animate_reading(index + 1)

        self._after_ids.append(self.root.after(200, step))

    def _finish_reading(self):
        value = self.model.value()
        self.result_var.set(str(value))
        self.caption_var.set(f"Новое число: {value}")
        self.mode = "done"
        self._after_ids.append(self.root.after(3000, self._show_change_button))

    def _show_change_button(self):
        if self.change_btn is not None:
            return
        self.change_btn = OvalButton(
            self.root, text="Изменить", command=self._on_change_click,
            width=150, height=52,
            bg="#b9d4f2", hover="#9cc3ec", text_color="#12406e",
            master_bg="#ffffff"
        )
        # чуть выше кнопки «Считать»
        self.change_btn.place(relx=1.0, rely=1.0, x=-30, y=-95, anchor="se")

    def _hide_change_button(self):
        if self.change_btn is not None:
            self.change_btn.destroy()
            self.change_btn = None

    def _on_change_click(self):
        self._hide_change_button()
        self.result_var.set("")
        self.caption_var.set("")
        self.mode = "edit"

    def run(self):
        self.root.mainloop()
