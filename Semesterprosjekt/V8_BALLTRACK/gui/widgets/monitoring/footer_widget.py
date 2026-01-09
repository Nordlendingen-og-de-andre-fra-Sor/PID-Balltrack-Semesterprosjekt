"""
footer_widget.py
---------------------------------------
En fleksibel statuslinje nederst i GUI.

Default felter:
    RAW, Pos, SP, U, Servo, Mode

Brukes av:
    main_window

Plassering:
    gui/widgets/monitoring/footer_widget.py
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("footer", "Preview – FooterWidget")

class FooterWidget(ttk.Frame, BaseWidget):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        BaseWidget.__init__(self)

        # Alle mulige felter vi kan vise i footer
        self.fields = {
            "raw":      {"label": "RAW",    "value": "---"},
            "pos":      {"label": "Pos",    "value": "---"},
            "sp":       {"label": "SP",     "value": "---"},
            "u":        {"label": "U",      "value": "---"},
            "servo_us": {"label": "Servo",  "value": "---"},
            "mode":     {"label": "Mode",   "value": "---"},
        }

        # Hvilke felter som skal vises (default)
        self.visible_fields = {
            "raw": True,
            "pos": True,
            "sp": True,
            "u": True,
            "servo_us": True,
            "mode": True,
        }

        self._build_ui()

    # ---------------------------------------------------------
    def _build_ui(self):
        """Bygger footer som en horisontal statuslinje."""
        self.labels = {}

        # Litt lys bakgrunn for statuslinje-look
        self.configure(padding=4)

        for key, entry in self.fields.items():
            frame = ttk.Frame(self)
            lbl_name = ttk.Label(frame, text=f"{entry['label']}:")
            lbl_val = ttk.Label(frame, text="---")

            lbl_name.pack(side="left")
            lbl_val.pack(side="left")

            self.labels[key] = (frame, lbl_val)

        self._render()

    # ---------------------------------------------------------
    def _render(self):
        """Render footer basert på hvilke felter som er synlige."""
        # Skjul alt
        for key, (frame, _) in self.labels.items():
            frame.pack_forget()

        # Vis kun de feltene som er aktivert
        for key, visible in self.visible_fields.items():
            if visible and key in self.labels:
                frame, _ = self.labels[key]
                frame.pack(side="left", padx=10)

    # ---------------------------------------------------------
    def set_visibility(self, key: str, state: bool):
        """Endrer hvilke felter som vises."""
        if key in self.visible_fields:
            self.visible_fields[key] = state
            self._render()

    # ---------------------------------------------------------
    def update_status(self, **kwargs):
        """
        Oppdaterer alle verdier i statuslinjen.

        Eksempel:
            footer.update(raw=770, pos=0.18, sp=0.21, u=0.11, servo_us=1550, mode="SIM")
        """
        for key, value in kwargs.items():
            if key in self.fields and key in self.labels:
                self.fields[key]["value"] = value
                _, lbl_val = self.labels[key]
                lbl_val.config(text=str(value))

    # ---------------------------------------------------------
    def bind(self, controller):
        """Forberedt for senere bruk hvis footer skal hente noe direkte fra controller."""
        super().bind(controller)

