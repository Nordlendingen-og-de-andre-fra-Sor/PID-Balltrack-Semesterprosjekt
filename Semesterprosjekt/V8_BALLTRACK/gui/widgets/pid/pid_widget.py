"""
pid_widget.py
---------------------------------------
PID-innstillinger for Balltrack Pi.

Tilpasset V7 + V5-basert PositionController med følgende API:

    controller.get_pid()        -> (kp, ki, kd)
    controller.set_pid(kp,ki,kd)
    controller.disable_integral(flag)
    controller.disable_derivative(flag)

Modusvelger (PID/PI/PD/P) er beholdt for pedagogikk, men brukes til
å slå av/på I- og D-leddet automatisk.
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget
from V8_BALLTRACK.controller.pid import PIDType

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("pid", "Preview – PIDWidget")

class PIDWidget(ttk.LabelFrame, BaseWidget):
    """
    Widget som presenterer og endrer PID-parametre i sanntid.

    GUI-elementer:
        - Tre inputfelter (Kp, Ki, Kd)
        - Modusvelger (P/PI/PD/PID)
        - Deaktiver I-ledd (I → ∞)
        - Deaktiver D-ledd (D → 0)
        - Apply-knapp
        - Reset-knapp
    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="PID-innstillinger")
        BaseWidget.__init__(self)

        self.var_pid_type = tk.StringVar(value=PIDType.PARALLEL.value)

        # Variabler for GUI-input
        self.var_kp = tk.StringVar()
        self.var_ki = tk.StringVar()
        self.var_kd = tk.StringVar()
        self.var_mode = tk.StringVar(value="PID")

        self.var_disable_i = tk.BooleanVar(value=False)
        self.var_disable_d = tk.BooleanVar(value=False)

        self._build_ui()

    # ---------------------------------------------------------
    def _build_ui(self):

        self.columnconfigure(1, weight=1)

        # --- PID FORM (øverst) ---
        ttk.Label(self, text="PID-form:").grid(row=0, column=0, sticky="w")
        self.combo_pid_type = ttk.Combobox(
            self,
            values=[p.value for p in PIDType],
            textvariable=self.var_pid_type,
            state="readonly",
            width=10
        )
        self.combo_pid_type.grid(row=0, column=1, sticky="ew", pady=2)

        # --- KP ---
        ttk.Label(self, text="Kp:").grid(row=1, column=0, sticky="w")
        self.entry_kp = ttk.Entry(self, textvariable=self.var_kp, width=10)
        self.entry_kp.grid(row=1, column=1, sticky="ew", pady=2)

        # --- KI ---
        ttk.Label(self, text="Ki:").grid(row=2, column=0, sticky="w")
        self.entry_ki = ttk.Entry(self, textvariable=self.var_ki, width=10)
        self.entry_ki.grid(row=2, column=1, sticky="ew", pady=2)

        # --- KD ---
        ttk.Label(self, text="Kd:").grid(row=3, column=0, sticky="w")
        self.entry_kd = ttk.Entry(self, textvariable=self.var_kd, width=10)
        self.entry_kd.grid(row=3, column=1, sticky="ew", pady=2)

        # --- MODUS ---
        ttk.Label(self, text="Modus:").grid(row=4, column=0, sticky="w")
        self.combo_mode = ttk.Combobox(
            self,
            values=["PID", "PI", "PD", "P"],
            textvariable=self.var_mode,
            state="readonly",
            width=8
        )
        self.combo_mode.grid(row=4, column=1, sticky="ew", pady=2)

        # --- I- og D-deaktivering ---
        self.chk_disable_i = ttk.Checkbutton(
            self,
            text="Sett I-ledd = ∞ (deaktiver I)",
            variable=self.var_disable_i
        )
        self.chk_disable_i.grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.chk_disable_d = ttk.Checkbutton(
            self,
            text="Sett D-ledd = 0 (deaktiver D)",
            variable=self.var_disable_d
        )
        self.chk_disable_d.grid(row=6, column=0, columnspan=2, sticky="w")

        # --- Apply/Reset ---
        frame_buttons = ttk.Frame(self)
        frame_buttons.grid(row=7, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(frame_buttons, text="Apply", command=self._apply).grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Reset", command=self._reset).grid(row=0, column=1, padx=5)
        
    # ---------------------------------------------------------
    # BINDING
    # ---------------------------------------------------------
    def bind(self, controller):
        BaseWidget.bind(self, controller)

        self._reset()

    # ---------------------------------------------------------
    # APPLY – send nye verdier til controller
    # ---------------------------------------------------------
    def _apply(self):

        if not self.controller:
            print("[PIDWidget] Ingen controller koblet.")
            return

        try:
            kp = float(self.var_kp.get())
            ki = float(self.var_ki.get())
            kd = float(self.var_kd.get())
        except ValueError:
            print("[PIDWidget] Feil: Kp/Ki/Kd må være tall.")
            return

        # 1. Sett PID-form: parallel / ideal / series
        try:
            pid_type = PIDType(self.var_pid_type.get())
        except ValueError:
            print("[PIDWidget] Feil: Ugyldig PID-form.")
            return

        if hasattr(self.controller, "set_pid_type"):
            self.controller.set_pid_type(pid_type)

        # 2. Sett PID-parametre
        if hasattr(self.controller, "set_pid"):
            self.controller.set_pid(kp, ki, kd)

        # 3. Bestem aktiv/deaktiv I og D basert på modus + checkbox
        mode = self.var_mode.get()

        disable_i = self.var_disable_i.get() or ("I" not in mode)
        disable_d = self.var_disable_d.get() or ("D" not in mode)

        # 4. Send I/D-status til controller
        if hasattr(self.controller, "disable_integral"):
            self.controller.disable_integral(disable_i)

        if hasattr(self.controller, "disable_derivative"):
            self.controller.disable_derivative(disable_d)

        print(
            f"[PIDWidget] Apply OK → "
            f"Form={pid_type.value}, "
            f"Kp={kp}, Ki={ki}, Kd={kd}, "
            f"Mode={mode}, "
            f"DisableI={disable_i}, DisableD={disable_d}"
        )

    # ---------------------------------------------------------
    # RESET – hent verdier fra controller
    # ---------------------------------------------------------
    def _reset(self):

        if not self.controller:
            print("[PIDWidget] Ingen controller tilgjengelig.")
            return

        # --- 1. Hent PID-parametre ---
        if hasattr(self.controller, "get_pid"):
            kp, ki, kd = self.controller.get_pid()
            self.var_kp.set(f"{kp}")
            self.var_ki.set(f"{ki}")
            self.var_kd.set(f"{kd}")

        # --- 2. Hent PID-type ---
        if hasattr(self.controller, "get_pid_type"):
            pid_type = self.controller.get_pid_type()
            self.var_pid_type.set(pid_type.value)

        # --- 3. Sett modus basert på Ki og Kd ---
        mode = "P"
        if ki != 0.0:
            mode += "I"
        if kd != 0.0:
            mode += "D"

        self.var_mode.set(mode)

        # --- 4. Synk checkboxer ---
        self.var_disable_i.set(ki == 0.0)
        self.var_disable_d.set(kd == 0.0)

        print(
            f"[PIDWidget] Reset OK → "
            f"Form={self.var_pid_type.get()}, "
            f"Kp={kp}, Ki={ki}, Kd={kd}, "
            f"Mode={mode}"
        )