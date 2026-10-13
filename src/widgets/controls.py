"""Виджеты интерфейса: вкладки систем и овальная кнопка."""

import tkinter as tk


def round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Нарисовать прямоугольник с закруглёнными углами."""
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class SystemTabs(tk.Canvas):
    """Плашка с выбором системы счисления."""

    def __init__(self, master, on_select, bg="#f1ccd7",
                 width=520, height=52, **kwargs):
        """Создать вкладки и сразу отрисовать их."""
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bd=0, bg=bg, **kwargs)
        self.on_select = on_select
        self.current = "binary"
        self.systems = [
            ("binary", "Двоичная"),
            ("balanced_ternary", "Троичная"),
            ("mixed", "Смешанная"),
        ]
        self._cw = width
        self._ch = height

        self.COLOR_BG = "#f7e4ec"
        self.COLOR_ACTIVE = "#e8b8ce"
        self.COLOR_IDLE = "#f7e4ec"
        self.COLOR_TEXT_ACTIVE = "#7a3d57"
        self.COLOR_TEXT_IDLE = "#a98298"

        self._build()

    def _build(self):
        """Нарисовать фон и сегменты вкладок."""
        round_rect(self, 0, 0, self._cw, self._ch, r=self._ch / 2,
                   fill=self.COLOR_BG, outline="", tags="pill")

        seg_w = self._cw / len(self.systems)
        self.segment_ids = {}
        self.text_ids = {}

        for i, (key, title) in enumerate(self.systems):
            x0 = i * seg_w
            x1 = x0 + seg_w
            seg_id = round_rect(
                self, x0 + 3, 3, x1 - 3, self._ch - 3,
                r=(self._ch - 6) / 2,
                fill=self.COLOR_IDLE, outline="", tags=("seg", key)
            )
            text_id = self.create_text(
                (x0 + x1) / 2, self._ch / 2, text=title,
                fill=self.COLOR_TEXT_IDLE,
                font=("Segoe UI Semibold", 11, "bold"),
                tags=("segtext", key)
            )
            self.segment_ids[key] = seg_id
            self.text_ids[key] = text_id
            self.tag_bind(key, "<Button-1>",
                          lambda e, k=key: self._select(k))
            self.tag_bind(key, "<Enter>",
                          lambda e, k=key: self._hover(k, True))
            self.tag_bind(key, "<Leave>",
                          lambda e, k=key: self._hover(k, False))
        self.configure(cursor="hand2")
        self._refresh()

    def _hover(self, key, on):
        """Подсветить сегмент при наведении мыши."""
        if key == self.current:
            return
        color = "#f1d5e0" if on else self.COLOR_IDLE
        self.itemconfigure(self.segment_ids[key], fill=color)

    def _select(self, key):
        """Обработать выбор системы пользователем."""
        if key == self.current:
            return
        self.current = key
        self._refresh()
        self.on_select(key)

    def _refresh(self):
        """Перекрасить сегменты в зависимости от активного."""
        for key in self.segment_ids:
            if key == self.current:
                self.itemconfigure(
                    self.segment_ids[key], fill=self.COLOR_ACTIVE)
                self.itemconfigure(
                    self.text_ids[key], fill=self.COLOR_TEXT_ACTIVE)
            else:
                self.itemconfigure(
                    self.segment_ids[key], fill=self.COLOR_IDLE)
                self.itemconfigure(
                    self.text_ids[key], fill=self.COLOR_TEXT_IDLE)


class OvalButton(tk.Canvas):
    """Кнопка-капсула с закруглёнными углами."""

    def __init__(self, master, text, command,
                 width=150, height=52,
                 bg="#e8b8ce", hover="#dba3bd",
                 text_color="#7a3d57",
                 master_bg="#f1ccd7", **kwargs):
        """Создать кнопку и сразу её нарисовать."""
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bd=0, bg=master_bg,
                         **kwargs)
        self.command = command
        self._bg = bg
        self._hover = hover
        self._fg = text_color
        self._cw = width
        self._ch = height
        self._build(text)

    def _build(self, text):
        """Нарисовать саму кнопку и подпись."""
        round_rect(self, 1, 1, self._cw - 1, self._ch - 1,
                   r=self._ch / 2,
                   fill=self._bg, outline="", tags="oval")
        self.create_text(self._cw / 2, self._ch / 2, text=text,
                         fill=self._fg,
                         font=("Segoe UI Semibold", 12, "bold"),
                         tags="label")
        for tag in ("oval", "label"):
            self.tag_bind(tag, "<Button-1>", lambda e: self.command())
            self.tag_bind(tag, "<Enter>",
                          lambda e: self.itemconfigure(
                              "oval", fill=self._hover))
            self.tag_bind(tag, "<Leave>",
                          lambda e: self.itemconfigure(
                              "oval", fill=self._bg))
        self.configure(cursor="hand2")

    def set_state(self, enabled):
        """Включить или выключить курсор-«руку» на кнопке."""
        self.configure(cursor="hand2" if enabled else "arrow")
