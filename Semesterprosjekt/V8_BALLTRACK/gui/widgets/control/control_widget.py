"""
control_widget.py
---------------------------------------
Del av Balltrack Pi GUI-systemet.

Formål:
    Tilby et enkelt brukergrensesnitt for:
        - Start av regulatoren
        - Stopp av regulatoren
        - Endring av settpunkt (SP)
        - Kjøring av servokalibrering

Brukes av:
    gui.main_window.BalltrackApp

Kalles når:
    BalltrackApp bygger GUI og binder widgeten til controlleren
    via bind(controller).

Ansvar:
    - Validering og formidling av brukerens kommandoer til controller
    - Håndtering av settpunkt-inndata
    - Gi tydelige, sikre brukeroperasjoner uten feilkollaps

Relasjoner:
    Kommuniserer direkte med:
        PositionController
            - set_setpoint()
            - start()
            - stop()
            - calibrate()
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("control", "Preview – ControlWidget")

class ControlWidget(ttk.LabelFrame, BaseWidget):
    """
    ControlWidget
    ---------------------------------------
    GUI-komponent for start/stop-kontroll og settpunktstyring.

    Arver fra:
        - ttk.LabelFrame (visuelt rammeelement)
        - BaseWidget (felles API og controller-binding)

    Metoder:
        bind(controller):
            Lagrer controller-objektet og leser initiale data.

        _start():
            Starter reguleringen via controlleren.

        _stop():
            Stopper reguleringen via controlleren.

        _calibrate():
            Kjører servokalibrering via controlleren.
    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Regulering")
        BaseWidget.__init__(self)

        self._build_ui()

    # ---------------------------------------------------------
    def _build_ui(self):
        """Minimal Start/Stop-modul."""

        self.btn_start = ttk.Button(self, text="Start regulering", command=self._start)
        self.btn_stop = ttk.Button(self, text="Stopp regulering", command=self._stop)

        self.btn_start.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_stop.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    def bind(self, controller):
        """Knytter widgeten til controller."""
        BaseWidget.bind(self, controller)


    # ---------------------------------------------------------
    def _start(self):
        if not self.controller:
            print("[ControlWidget] Ingen controller.")
            return

        if hasattr(self.controller, "start"):
            self.controller.start()

        print("[ControlWidget] Regulering aktivert.")

    # ---------------------------------------------------------
    def _stop(self):
        if not self.controller:
            print("[ControlWidget] Ingen controller.")
            return

        if hasattr(self.controller, "stop"):
            self.controller.stop()

        print("[ControlWidget] Regulering stoppet.")
