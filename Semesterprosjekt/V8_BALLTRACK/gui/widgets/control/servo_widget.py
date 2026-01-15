"""
servo_widget.py
---------------------------------------
Widget for visning og manuell styring av servoens posisjon.

Tilpasset PositionController (V5/V7/V8) med API:

    enable_manual_servo(flag: bool)
    set_servo_manual(value_norm: float)
    get_servo_position() -> float

Designmål:
- "Faceplate"-stil: tydelig status + enkel manuell overstyring.
- Manuell styring overstyrer PID-regulering.
- Slider er kun aktiv i manuell modus.
- Robust mot at ttk.Scale trigges ved programmatisk .set()
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
    - refresh() kan kalles periodisk fra AppScreen for live oppdatering i AUTO
    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Servo")
        BaseWidget.__init__(self)

        # Visning i prosent (0..100)
        self.var_pos = tk.DoubleVar(value=50.0)
        # Manuell modus
        self.var_manual = tk.BooleanVar(value=False)

        # Intern guard for å unngå at slider-callback trigges ved .set()
        self._ignore_slider_callback = False

        self._build_ui()
        self._apply_manual_ui_state(False)

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def _build_ui(self):
        # Status-linje
        ttk.Label(self, text="Servo posisjon:").grid(row=0, column=0, sticky="w")
        self.lbl_pos = ttk.Label(self, text="50 %")
        self.lbl_pos.grid(row=0, column=1, sticky="e")

        # Manuell toggle
        self.chk_manual = ttk.Checkbutton(
            self,
            text="Manuell styring",
            variable=self.var_manual,
            command=self._manual_changed,
        )
        self.chk_manual.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Slider for manuell styring
        self.slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            command=self._slider_moved,
            length=300,
        )
        self.slider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)

        self.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    # Binding
    # ---------------------------------------------------------
    def bind(self, controller):
        super().bind(controller)

        # Start alltid i AUTO ved bind (forutsigbar faceplate)
        self.var_manual.set(False)
        self._apply_manual_ui_state(False)

        # Initial status fra controller
        self._sync_from_controller()

    # ---------------------------------------------------------
    # Periodisk refresh (kalles fra AppScreen)
    # ---------------------------------------------------------
    def refresh(self):
        """
        Oppdaterer visning fra controller.
        I manuell modus lar vi operatør styre uten at AUTO overskriver slider/label.
        """
        if self.var_manual.get():
            return
        self._sync_from_controller()

    # ---------------------------------------------------------
    # Intern: Sync controller -> UI
    # ---------------------------------------------------------
    def _sync_from_controller(self):
        if not self.controller:
            return
        if not hasattr(self.controller, "get_servo_position"):
            return

        try:
            pos_norm = float(self.controller.get_servo_position())
        except Exception:
            return

        pos_norm = max(0.0, min(1.0, pos_norm))
        pos_percent = pos_norm * 100.0

        self.var_pos.set(pos_percent)
        self.lbl_pos.config(text=f"{int(round(pos_percent))} %")

        # Unngå å trigge slider-callback når vi setter verdi programmatisk
        self._ignore_slider_callback = True
        try:
            self.slider.set(pos_percent)
        finally:
            self._ignore_slider_callback = False

    # ---------------------------------------------------------
    # Intern: UI-state ved manual ON/OFF
    # ---------------------------------------------------------
    def _apply_manual_ui_state(self, is_manual: bool):
        if is_manual:
            self.slider.state(["!disabled"])
        else:
            self.slider.state(["disabled"])

    # ---------------------------------------------------------
    # Manual toggle
    # ---------------------------------------------------------
    def _manual_changed(self):
        """
        Aktiverer/deaktiverer manuell styring.
        - Varsler controller
        - Aktiverer/deaktiverer slider
        - Ved OFF: synkroniser tilbake til aktuell servo-pos
        """
        is_manual = bool(self.var_manual.get())

        # 1) Varsle controller først (ryddig for logging/feilsøking)
        if self.controller and hasattr(self.controller, "enable_manual_servo"):
            try:
                self.controller.enable_manual_servo(is_manual)
            except Exception:
                pass

        # 2) Oppdater UI-state
        self._apply_manual_ui_state(is_manual)

        # 3) Hvis vi går tilbake til AUTO: hent posisjon fra controller igjen
        if not is_manual:
            self._sync_from_controller()

    # ---------------------------------------------------------
    # Slider -> Controller
    # ---------------------------------------------------------
    def _slider_moved(self, value):
        """
        Sender manuell servo-posisjon til controller.
        GUI: 0–100 %, controller forventer 0.0–1.0
        """
        # Guard: ikke send i AUTO
        if not self.var_manual.get():
            return

        # Guard: ikke send hvis slider ble satt programmatisk
        if self._ignore_slider_callback:
            return

        try:
            pos_percent = float(value)
        except Exception:
            return

        pos_percent = max(0.0, min(100.0, pos_percent))
        self.var_pos.set(pos_percent)
        self.lbl_pos.config(text=f"{int(round(pos_percent))} %")

        if self.controller and hasattr(self.controller, "set_servo_manual"):
            try:
                self.controller.set_servo_manual(pos_percent / 100.0)
            except Exception:
                pass
