import tkinter as tk


class SystemTabs(tk.Canvas):
    # общий полупрозрачный овал-«таблетка» с выбором системы

    def __init__(self, master, on_select, bg="#ffffff",
                 width=520, height=52, **kwargs):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bd=0, bg=bg, **kwargs)
        self.on_select = on_select
        self.current = "binary"
        self.systems = [
            ("binary", "Двоичная"),
            ("balanced_ternary", "Троичная"),
            ("mixed", "Смешанная"),
        ]
        # ВАЖНО: не _w / _h — они заняты внутри tk.Canvas
        self._cw = width
        self._ch = height

        self.COLOR_BG = "#eef3fa"
        self.COLOR_ACTIVE = "#b9d4f2"
        self.COLOR_IDLE = "#eef3fa"
        self.COLOR_TEXT_ACTIVE = "#12406e"
        self.COLOR_TEXT_IDLE = "#6b7c93"

        self._build()

    def _build(self):
        self.create_oval(0, 0, self._cw, self._ch,
                         fill=self.COLOR_BG, outline="", tags="pill")

        seg_w = self._cw / len(self.systems)
        self.segment_ids = {}
        self.text_ids = {}

        for i, (key, title) in enumerate(self.systems):
            x0 = i * seg_w
            x1 = x0 + seg_w
            sid = self.create_oval(
                x0 + 3, 3, x1 - 3, self._ch - 3,
                fill=self.COLOR_IDLE, outline="", tags=("seg", key)
            )
            tid = self.create_text(
                (x0 + x1) / 2, self._ch / 2, text=title,
                fill=self.COLOR_TEXT_IDLE,
                font=("Segoe UI Semibold", 11, "bold"),
                tags=("segtext", key)
            )
            self.segment_ids[key] = sid
            self.text_ids[key] = tid
            self.tag_bind(key, "<Button-1>", lambda e, k=key: self._select(k))
            self.tag_bind(key, "<Enter>",
                          lambda e, k=key: self._hover(k, True))
            self.tag_bind(key, "<Leave>",
                          lambda e, k=key: self._hover(k, False))
        self.configure(cursor="hand2")
        self._refresh()

    def _hover(self, key, on):
        if key == self.current:
            return
        color = "#e3ecf7" if on else self.COLOR_IDLE
        self.itemconfigure(self.segment_ids[key], fill=color)

    def _select(self, key):
        if key == self.current:
            return
        self.current = key
        self._refresh()
        self.on_select(key)

    def _refresh(self):
        for key in self.segment_ids:
            if key == self.current:
                self.itemconfigure(self.segment_ids[key], fill=self.COLOR_ACTIVE)
                self.itemconfigure(self.text_ids[key], fill=self.COLOR_TEXT_ACTIVE)
            else:
                self.itemconfigure(self.segment_ids[key], fill=self.COLOR_IDLE)
                self.itemconfigure(self.text_ids[key], fill=self.COLOR_TEXT_IDLE)


class OvalButton(tk.Canvas):
    # полупрозрачная овальная кнопка

    def __init__(self, master, text, command,
                 width=140, height=48,
                 bg="#b9d4f2", hover="#9cc3ec", text_color="#12406e",
                 master_bg="#ffffff", **kwargs):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bd=0, bg=master_bg, **kwargs)
        self.command = command
        self._bg = bg
        self._hover = hover
        self._fg = text_color
        # тоже не _w / _h
        self._cw = width
        self._ch = height
        self._build(text)

    def _build(self, text):
        self.create_oval(1, 1, self._cw - 1, self._ch - 1,
                         fill=self._bg, outline="", tags="oval")
        self.create_text(self._cw / 2, self._ch / 2, text=text,
                         fill=self._fg,
                         font=("Segoe UI Semibold", 12, "bold"),
                         tags="label")
        for tag in ("oval", "label"):
            self.tag_bind(tag, "<Button-1>", lambda e: self.command())
            self.tag_bind(tag, "<Enter>",
                          lambda e: self.itemconfigure("oval", fill=self._hover))
            self.tag_bind(tag, "<Leave>",
                          lambda e: self.itemconfigure("oval", fill=self._bg))
        self.configure(cursor="hand2")

    def set_state(self, enabled):
        self.configure(cursor="hand2" if enabled else "arrow")
