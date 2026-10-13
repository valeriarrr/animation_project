"""Главное окно приложения «Двоичные числа»."""

import tkinter as tk
from tkinter import font as tkfont

from src.models.number_model import NumberModel
from src.renderers.renderer import Renderer
from src.widgets.controls import SystemTabs, OvalButton


class App:
    """Собирает окно, обрабатывает клики и запускает считывание."""

    def __init__(self):
        """Создать окно и собрать интерфейс."""
        self.root = tk.Tk()
        self.root.title("Двоичные числа — Рошевских В.И., ПИ25-1")
        self.root.geometry("820x540")
        self.root.configure(bg="#f1ccd7")

        self.model = NumberModel(size=8)
        self.mode = "edit"
        self._after_ids = []
        self.change_btn = None

        self._build_ui()

    def _build_ui(self):
        """Создать и разместить все виджеты окна."""
        title_font = tkfont.Font(family="Segoe UI Semibold",
                                 size=22, weight="bold")
        tk.Label(
            self.root, text="ДВОИЧНЫЕ ЧИСЛА",
            bg="#f1ccd7", fg="#7a3d57", font=title_font
        ).pack(pady=(18, 0))

        self.tabs = SystemTabs(self.root,
                               on_select=self._on_system_change,
                               bg="#f1ccd7")
        self.tabs.pack(pady=(12, 0))

        self.canvas = tk.Canvas(self.root, width=780, height=170,
                                bg="#f1ccd7", highlightthickness=0)
        self.canvas.pack(pady=(10, 0))
        self.renderer = Renderer(self.canvas, self.model)
        self.renderer.draw_all()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        self.result_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.result_var,
            bg="#f1ccd7", fg="#7a3d57",
            font=tkfont.Font(family="Segoe UI",
                             size=48, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=40, pady=(8, 0))

        self.caption_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.caption_var,
            bg="#f1ccd7", fg="#a98298",
            font=("Segoe UI", 11), anchor="w"
        ).pack(fill="x", padx=40)

        self.read_btn = OvalButton(
            self.root, text="Считать",
            command=self._on_read_click,
            width=150, height=52,
            bg="#e8b8ce", hover="#dba3bd",
            text_color="#7a3d57",
            master_bg="#f1ccd7"
        )
        self.read_btn.place(relx=1.0, rely=1.0,
                            x=-30, y=-30, anchor="se")

    def _on_system_change(self, system):
        """Переключить систему счисления и обновить холст."""
        self.model.set_system(system)
        self.renderer.draw_all()
        self.result_var.set("")
        self.caption_var.set("")
        self.mode = "edit"
        self._hide_change_button()

    def _on_canvas_click(self, event):
        """Обработать клик по кружку-регистру."""
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
        """Запустить анимацию считывания."""
        if self.mode != "edit":
            return
        self.mode = "reading"
        self.result_var.set("")
        self.caption_var.set("")
        self._hide_change_button()
        self._animate_reading(0)

    def _animate_reading(self, index):
        """Подсветить регистр с индексом index и перейти к следующему."""
        if index >= self.model.size:
            self._finish_reading()
            return
        color = Renderer.HIGHLIGHT_COLORS[
            index % len(Renderer.HIGHLIGHT_COLORS)
        ]
        self.renderer.highlight_register(index, color)

        def step():
            self.renderer.reset_register_color(index)
            self._animate_reading(index + 1)

        self._after_ids.append(self.root.after(200, step))

    def _finish_reading(self):
        """Показать результат и запланировать кнопку «Изменить»."""
        value = self.model.value()
        self.result_var.set(str(value))
        self.caption_var.set(f"Новое число: {value}")
        self.mode = "done"
        self._after_ids.append(
            self.root.after(3000, self._show_change_button)
        )

    def _show_change_button(self):
        """Показать овальную кнопку «Изменить»."""
        if self.change_btn is not None:
            return
        self.change_btn = OvalButton(
            self.root, text="Изменить",
            command=self._on_change_click,
            width=150, height=52,
            bg="#e8b8ce", hover="#dba3bd",
            text_color="#7a3d57",
            master_bg="#f1ccd7"
        )
        self.change_btn.place(relx=1.0, rely=1.0,
                              x=-30, y=-95, anchor="se")

    def _hide_change_button(self):
        """Скрыть кнопку «Изменить», если она есть."""
        if self.change_btn is not None:
            self.change_btn.destroy()
            self.change_btn = None

    def _on_change_click(self):
        """Вернуть приложение в режим редактирования."""
        self._hide_change_button()
        self.result_var.set("")
        self.caption_var.set("")
        self.mode = "edit"

    def run(self):
        """Запустить главный цикл окна."""
        self.root.mainloop()
