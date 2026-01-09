"""
servo_widget.py
---------------------------------------
Widget for visning og manuell styring av servoens posisjon.
Tilpasset PositionController (V5/V7) med:

    enable_manual_servo(flag)
    set_servo_manual(value_norm)
    get_servo_position()

Manuell styring deaktiverer automatisk PID-regulering.
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("servo", "Preview – ServoWidget")

class ServoWidget(ttk.LabelFrame, BaseWidget):
    """
    ServoWidget – viser servoens posisjon og tillater manuell styring.

    - Viser posisjon i prosent (0–100 %)
    - Manuell styring overstyrer PID helt
    - Slider aktiv kun i manuell modus
    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Servo")
        BaseWidget.__init__(self)

        self.var_pos = tk.DoubleVar(value=50)     # visning (0–100 %)
        self.var_manual = tk.BooleanVar(value=False)

        self._build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def _build_ui(self):

        # Label som viser nåværende servo-posisjon
        ttk.Label(self, text="Servo posisjon:").grid(row=0, column=0, sticky="w")
        self.lbl_pos = ttk.Label(self, text="50 %")
        self.lbl_pos.grid(row=0, column=1, sticky="e")

        # Checkbox for å aktivere manuell styring
        self.chk_manual = ttk.Checkbutton(
            self,
            text="Manuell styring",
            variable=self.var_manual,
            command=self._manual_changed
        )
        self.chk_manual.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Slider for manuell styring
        self.slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            command=self._slider_moved,
            length=300
        )
        self.slider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        self.slider.state(["disabled"])  # Kun aktiv i manuell modus

        self.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    # BINDING
    # ---------------------------------------------------------
    def bind(self, controller):
        super().bind(controller)

        # Initial posisjon fra controller
        if hasattr(self.controller, "get_servo_position"):
            pos = float(self.controller.get_servo_position()) * 100
            self.var_pos.set(pos)
            self.lbl_pos.config(text=f"{int(pos)} %")
            self.slider.set(pos)

    # ---------------------------------------------------------
    # ENDRE MANUELL MODUS
    # ---------------------------------------------------------
    def _manual_changed(self):
        """
        Aktiverer eller deaktiverer manuell styring.
        Manuell styring overstyrer PID-reguleringen.
        """

        is_manual = self.var_manual.get()

        # Aktiver/deaktiver slider
        if is_manual:
            self.slider.state(["!disabled"])
        else:
            self.slider.state(["disabled"])
            # Hent posisjon fra PID igjen
            if hasattr(self.controller, "get_servo_position"):
                pos = float(self.controller.get_servo_position()) * 100
                self.var_pos.set(pos)
                self.lbl_pos.config(text=f"{int(pos)} %")
                self.slider.set(pos)

        # Varsle controller
        if hasattr(self.controller, "enable_manual_servo"):
            self.controller.enable_manual_servo(is_manual)

    # ---------------------------------------------------------
    # SLIDER → CONTROLLER
    # ---------------------------------------------------------
    def _slider_moved(self, value):
        """
        Sende manuell servo-posisjon til controller.
        Verdien er 0–100 %, controller forventer 0.0–1.0.
        """

        pos_percent = float(value)
        self.var_pos.set(pos_percent)
        self.lbl_pos.config(text=f"{int(pos_percent)} %")

        if self.controller and hasattr(self.controller, "set_servo_manual"):
            # Konverter prosent → normalisert verdi
            self.controller.set_servo_manual(pos_percent / 100.0)
