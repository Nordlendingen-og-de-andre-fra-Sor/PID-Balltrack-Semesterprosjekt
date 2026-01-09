"""
setpoint_widget.py
---------------------------------------
Widget for visning og justering av settpunkt (0–1).

Brukes av:
    ControlWidget og main_window.

Kalles når:
    - slider beveges
    - bruker skriver verdi
    - controller endrer settpunkt
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("setpoint", "Preview – SetpointWidget")

class SetpointWidget(ttk.LabelFrame, BaseWidget):
    def __init__(self, parent):
        super().__init__(parent, text="Settpunkt")
        BaseWidget.__init__(self)

        self.var_sp = tk.DoubleVar(value=0.5)

        self._build_ui()

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------
    def _build_ui(self):
        # --- Kolonnekonfigurasjon ---
        # 0 = Label
        # 1 = Entry (skal IKKE strekke seg)
        # 2 = Ekstra kolonne som slider kan bruke til fleks
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        # Label
        ttk.Label(self, text="SP:").grid(row=0, column=0, sticky="w")

        # Entry (fast størrelse)
        self.entry = ttk.Entry(self, width=6, textvariable=self.var_sp)
        self.entry.grid(row=0, column=1, sticky="w", padx=(5, 10))

        # Slider (full bredde via kolonne 2)
        self.slider = ttk.Scale(
            self,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            command=self._slider_changed,
        )
        self.slider.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        # Entry bindings
        self.entry.bind("<Return>", self._entry_changed)
        self.entry.bind("<FocusOut>", self._entry_changed)



    # ---------------------------------------------------------
    # Slider → entry → controller (prosentvis)
    # ---------------------------------------------------------
    def _slider_changed(self, value):
        sp_float = float(value)             # 0.0–1.0
        sp_percent = int(sp_float * 100)    # 0–100 %

        self.var_sp.set(sp_percent)

        if self.controller and hasattr(self.controller, "set_setpoint"):
            self.controller.set_setpoint(sp_float)


    # ---------------------------------------------------------
    # Entry → slider → controller
    # ---------------------------------------------------------
    def _entry_changed(self, event):
        try:
            sp_percent = int(self.var_sp.get())
        except ValueError:
            return

        sp_percent = max(0, min(100, sp_percent))
        sp_float = sp_percent / 100.0

        self.slider.set(sp_float)

        if self.controller and hasattr(self.controller, "set_setpoint"):
            self.controller.set_setpoint(sp_float)


    # ---------------------------------------------------------
    # Controller → widget
    # ---------------------------------------------------------
    def bind(self, controller):
        super().bind(controller)

        if hasattr(self.controller, "get_setpoint"):
            sp_float = float(self.controller.get_setpoint())
            sp_percent = int(sp_float * 100)

            self.var_sp.set(sp_percent)
            self.slider.set(sp_float)
