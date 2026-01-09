"""
log_widget.py
---------------------------------------
Del av Balltrack Pi GUI-systemet.

Formål:
    Tilby en enkel og funksjonell loggvisning i GUI-et, samt mulighet
    for å lagre loggen til fil og tømme den ved behov.

Brukes av:
    gui.main_window.BalltrackApp

Kalles når:
    BalltrackApp oppdaterer loggdata i _controller_update().

Ansvar:
    - Vise tekstlogg i et scrollbar-basert tekstfelt
    - Legge til nye logglinjer med tidsstempel
    - Slette all logg (clear)
    - Lagre logg til fil (save_log)

Relasjoner:
    Motta tekststreng fra:
        - BalltrackApp._controller_update()
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime

from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("log", "Preview – LogWidget")

class LogWidget(ttk.LabelFrame, BaseWidget):
    """
    LogWidget
    ---------------------------------------
    Widget for å vise og lagre tekstlogg.

    Funksjoner:
        - write(text): legger til en linje i loggvinduet
        - clear(): tømmer loggen
        - save_log(): lagrer innhold til valgfri fil

    Bruker:
        - tidsstemplet logg (HH:MM:SS)
        - read-only tekstfelt (brukeren kan ikke redigere manuelt)
    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Logg")
        BaseWidget.__init__(self)

        self._build_ui()

    # ---------------------------------------------------------
    # UI-BYGGING
    # ---------------------------------------------------------
    def _build_ui(self):
        """Bygger tekstfelt, scrollbar og knapper."""

        # Tekstområde (read-only)
        self.text = tk.Text(
            self,
            height=10,
            wrap="word",
            state="disabled",
            bg="#1e1e1e",
            fg="#d0d0d0",
            insertbackground="white",
        )
        self.text.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.text.yview
        )
        self.text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky="ns")

        # Knapper
        ttk.Button(self, text="Clear", command=self.clear).grid(
            row=1, column=0, sticky="ew", padx=2, pady=3
        )
        ttk.Button(self, text="Lagre", command=self.save_log).grid(
            row=1, column=1, sticky="ew", padx=2, pady=3
        )

        # Stretch i grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    # ---------------------------------------------------------
    # LOGGFØRING
    # ---------------------------------------------------------
    def write(self, text: str):
        """
        Legger til en linje i loggvinduet med tidsstempel.

        Parametre:
            text (str): tekst som skal logges
        """

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # Gjør widget skrivbar
        self.text.configure(state="normal")
        self.text.insert("end", f"[{timestamp}] {text}\n")
        self.text.configure(state="disabled")

        # Scroll automatisk ned
        self.text.see("end")

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------
    def clear(self):
        """Tømmer loggvinduet."""
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    # ---------------------------------------------------------
    # SAVE TO FILE
    # ---------------------------------------------------------
    def save_log(self):
        """
        Lagrer logginnholdet til en tekstfil valgt av brukeren.

        Feil håndteres trygt slik at GUI ikke krasjer.
        """

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All files", "*.*")],
            title="Lagre logg som..."
        )

        if not file_path:
            return  # Bruker avbrøt

        try:
            content = self.text.get("1.0", "end")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"[LogWidget] Logg lagret: {file_path}")

        except Exception as e:
            print(f"[LogWidget] FEIL ved lagring: {e}")
