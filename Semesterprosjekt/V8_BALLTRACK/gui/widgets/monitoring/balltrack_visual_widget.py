"""
balltrack_visual_widget.py
---------------------------------------
Digital visuell representasjon av ballens posisjon.

Plassering:
    gui/widgets/monitoring/

Formål:
    Vise en horisontal track og en rød ball som flytter seg
    i henhold til posisjon (0–1) fra controlleren.

Brukes av:
    main_window (rett under SetpointWidget)
"""

import tkinter as tk
from tkinter import ttk
from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("visual", "Preview – BalltrackVisualWidget")

class BalltrackVisualWidget(ttk.LabelFrame, BaseWidget):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Balltrack")
        BaseWidget.__init__(self)

        self.canvas_height = 80
        self.ball_radius = 10
        self._last_pos = 0.5     # husk sist posisjon for resizing

        self._build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def _build_ui(self):
        # Canvas uten fast bredde — følger vinduet
        self.canvas = tk.Canvas(
            self,
            height=self.canvas_height,
            bg="#f5f5f5",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.canvas.pack(fill="x", padx=10, pady=10)

        # Bind resizing
        self.canvas.bind("<Configure>", self._redraw)

        # Start med første tegning
        self._redraw()

    # ---------------------------------------------------------
    # Redraw når canvas endrer størrelse
    # ---------------------------------------------------------
    def _redraw(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas_height

        self.canvas.delete("all")

        # Track-grenser
        self.x_min = 20
        self.x_max = max(40, width - 20)   # unngå negativ bredde
        self.track_y = height // 2

        # Track-linje
        self.track = self.canvas.create_line(
            self.x_min,
            self.track_y,
            self.x_max,
            self.track_y,
            width=4,
            fill="black"
        )

        # Ballposisjon basert på _last_pos
        x = self._pos_to_canvas(self._last_pos)

        self.ball = self.canvas.create_oval(
            x - self.ball_radius,
            self.track_y - self.ball_radius,
            x + self.ball_radius,
            self.track_y + self.ball_radius,
            fill="red"
        )

    # ---------------------------------------------------------
    # Posisjonsberegning
    # ---------------------------------------------------------
    def _pos_to_canvas(self, pos: float):
        pos = max(0.0, min(1.0, pos))
        return self.x_min + pos * (self.x_max - self.x_min)

    # ---------------------------------------------------------
    # Ekstern API – oppdatere posisjon
    # ---------------------------------------------------------
    def set_position(self, pos: float):
        """Setter ballens posisjon (0–1 skala)."""
        self._last_pos = max(0.0, min(1.0, pos))  # husk sist posisjon

        # Canvas må være tegnet først
        if not hasattr(self, "ball"):
            return

        x = self._pos_to_canvas(self._last_pos)

        self.canvas.coords(
            self.ball,
            x - self.ball_radius,
            self.track_y - self.ball_radius,
            x + self.ball_radius,
            self.track_y + self.ball_radius
        )

    # ---------------------------------------------------------
    # Bind controller → widget
    # ---------------------------------------------------------
    def bind(self, controller):
        super().bind(controller)

        if hasattr(self.controller, "get_servo_position"):
            pos = self.controller.get_servo_position()
            self.set_position(pos)

