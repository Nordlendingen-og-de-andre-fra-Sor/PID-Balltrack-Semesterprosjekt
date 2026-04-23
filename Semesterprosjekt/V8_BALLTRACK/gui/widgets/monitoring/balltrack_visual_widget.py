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

        self.canvas_height = 120
        self.ball_radius = 10
        self._last_pos = 0.5

        self.var_pos = tk.StringVar(value="Posisjon: 0.500")
        self.var_raw = tk.StringVar(value="RAW: ---")
        self.var_sp = tk.StringVar(value="SP: 0.500")

        self._build_ui()

    def _build_ui(self):
        info_frame = ttk.Frame(self)
        info_frame.pack(fill="x", padx=10, pady=(8, 0))

        ttk.Label(info_frame, textvariable=self.var_pos).pack(side="left", padx=(0, 15))
        ttk.Label(info_frame, textvariable=self.var_raw).pack(side="left", padx=(0, 15))
        ttk.Label(info_frame, textvariable=self.var_sp).pack(side="left")

        self.canvas = tk.Canvas(
            self,
            height=self.canvas_height,
            bg="#f5f5f5",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas.bind("<Configure>", self._redraw)
        self._redraw()

    def _redraw(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas_height

        self.canvas.delete("all")

        self.x_min = 20
        self.x_max = max(40, width - 20)
        self.track_y = height // 2

        self.canvas.create_line(
            self.x_min,
            self.track_y,
            self.x_max,
            self.track_y,
            width=4,
            fill="black"
        )

        x = self._pos_to_canvas(self._last_pos)

        self.ball = self.canvas.create_oval(
            x - self.ball_radius,
            self.track_y - self.ball_radius,
            x + self.ball_radius,
            self.track_y + self.ball_radius,
            fill="red"
        )

    def _pos_to_canvas(self, pos: float):
        pos = max(0.0, min(1.0, pos))
        return self.x_min + pos * (self.x_max - self.x_min)

    def set_position(self, pos: float):
        self._last_pos = max(0.0, min(1.0, pos))

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

    def bind(self, controller):
        BaseWidget.bind(self, controller)

        if hasattr(self.controller, "get_status"):
            status = self.controller.get_status()
            self.update_status(status)

            
    def update_status(self, status: dict):
        pos = status.get("pos", None)

        if pos is None:
            return

        try:
            pos = float(pos)
        except Exception:
            return

        self.set_position(pos)