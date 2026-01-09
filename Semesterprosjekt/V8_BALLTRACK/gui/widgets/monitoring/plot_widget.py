"""
plot_widget.py
---------------------------------------
Utvidet plott-widget med 6 kurver:
SP, PV, u_tot, u_P, u_I, u_D
"""

import tkinter as tk
from tkinter import ttk
import time

from V8_BALLTRACK.gui.widgets.base_widget import BaseWidget


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from V8_BALLTRACK.gui.widgets.registry import register_widget

@register_widget("plot", "Preview – PlotWidget")

class PlotWidget(ttk.LabelFrame, BaseWidget):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Plot")
        BaseWidget.__init__(self)

        # Dataserier
        self.timestamps = []
        self.data_sp = []
        self.data_pv = []
        self.data_u_tot = []
        self.data_u_p = []
        self.data_u_i = []
        self.data_u_d = []

        self.time_window = 10.0

        self._build_ui()
        self._build_plot()

    # ---------------------------------------------------------
    # UI-KOMPONENTER
    # ---------------------------------------------------------
    def _build_ui(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_top, text="Tidsvindu (sek):").pack(side="left")
        self.cmb_window = ttk.Combobox(
            frame_top, values=["5", "10", "20", "30", "60"],
            width=5, state="readonly"
        )
        self.cmb_window.set("10")
        self.cmb_window.pack(side="left", padx=5)
        self.cmb_window.bind("<<ComboboxSelected>>", self._window_changed)

        self.var_autoscale = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_top, text="Autoscale",
                        variable=self.var_autoscale).pack(side="left", padx=10)

        ttk.Button(frame_top, text="Clear", command=self._clear).pack(side="right")

        # ---------------------------
        # Kurvevalg (checkboxes)
        # ---------------------------
        self.frame_curve = ttk.Frame(self)
        self.frame_curve.pack(fill="x", padx=5, pady=3)

        self.var_show_sp = tk.BooleanVar(value=True)
        self.var_show_pv = tk.BooleanVar(value=True)
        self.var_show_u_tot = tk.BooleanVar(value=True)
        self.var_show_u_p = tk.BooleanVar(value=False)
        self.var_show_u_i = tk.BooleanVar(value=False)
        self.var_show_u_d = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.frame_curve, text="Setpoint", variable=self.var_show_sp,
                        command=self._update_curve_visibility).pack(side="left")
        ttk.Checkbutton(self.frame_curve, text="PV", variable=self.var_show_pv,
                        command=self._update_curve_visibility).pack(side="left")
        ttk.Checkbutton(self.frame_curve, text="u_tot", variable=self.var_show_u_tot,
                        command=self._update_curve_visibility).pack(side="left")
        ttk.Checkbutton(self.frame_curve, text="u_P", variable=self.var_show_u_p,
                        command=self._update_curve_visibility).pack(side="left")
        ttk.Checkbutton(self.frame_curve, text="u_I", variable=self.var_show_u_i,
                        command=self._update_curve_visibility).pack(side="left")
        ttk.Checkbutton(self.frame_curve, text="u_D", variable=self.var_show_u_d,
                        command=self._update_curve_visibility).pack(side="left")

    # ---------------------------------------------------------
    # PLOTTING – MATPLOTLIB
    # ---------------------------------------------------------
    def _build_plot(self):
        self.fig = Figure(figsize=(6, 3), dpi=100)

        # Gi plass for legend
        self.fig.subplots_adjust(right=0.82)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel("Verdi")
        self.ax.set_xlabel("Tid (sek)")

        # Kurver
        self.line_sp,     = self.ax.plot([], [], color="#D32F2F", label="Setpoint")
        self.line_pv,     = self.ax.plot([], [], color="#1976D2", label="PV")
        self.line_u_tot,  = self.ax.plot([], [], color="#FFC107", label="u_tot")
        self.line_u_p,    = self.ax.plot([], [], color="#388E3C", label="u_P")
        self.line_u_i,    = self.ax.plot([], [], color="#FF9800", label="u_I")
        self.line_u_d,    = self.ax.plot([], [], color="#9C27B0", label="u_D")

        # Fast legend på høyre side
        self.ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # VIS / SKJUL KURVER
    # ---------------------------------------------------------
    def _update_curve_visibility(self):
        self.line_sp.set_visible(self.var_show_sp.get())
        self.line_pv.set_visible(self.var_show_pv.get())
        self.line_u_tot.set_visible(self.var_show_u_tot.get())
        self.line_u_p.set_visible(self.var_show_u_p.get())
        self.line_u_i.set_visible(self.var_show_u_i.get())
        self.line_u_d.set_visible(self.var_show_u_d.get())

        self.canvas.draw_idle()

    # ---------------------------------------------------------
    # OPPDATER DATA
    # ---------------------------------------------------------
    def update_plot(self, sp, pv, u_tot, u_p, u_i, u_d):
        now = time.time()

        self.timestamps.append(now)
        self.data_sp.append(sp)
        self.data_pv.append(pv)
        self.data_u_tot.append(u_tot)
        self.data_u_p.append(u_p)
        self.data_u_i.append(u_i)
        self.data_u_d.append(u_d)

        self._trim_data(now)

        # Relative time
        t0 = self.timestamps[0]
        t_rel = [t - t0 for t in self.timestamps]

        # Sett datasett
        self.line_sp.set_data(t_rel, self.data_sp)
        self.line_pv.set_data(t_rel, self.data_pv)
        self.line_u_tot.set_data(t_rel, self.data_u_tot)
        self.line_u_p.set_data(t_rel, self.data_u_p)
        self.line_u_i.set_data(t_rel, self.data_u_i)
        self.line_u_d.set_data(t_rel, self.data_u_d)

        # Autoscale
        if self.var_autoscale.get():
            self.ax.relim()
            self.ax.autoscale_view()

        self.ax.set_xlim(0, self.time_window)

        self.canvas.draw_idle()

    # ---------------------------------------------------------
    def _trim_data(self, now):
        while self.timestamps and now - self.timestamps[0] > self.time_window:
            self.timestamps.pop(0)
            self.data_sp.pop(0)
            self.data_pv.pop(0)
            self.data_u_tot.pop(0)
            self.data_u_p.pop(0)
            self.data_u_i.pop(0)
            self.data_u_d.pop(0)

    def _window_changed(self, event=None):
        self.time_window = float(self.cmb_window.get())

    def _clear(self):
        self.timestamps.clear()
        self.data_sp.clear()
        self.data_pv.clear()
        self.data_u_tot.clear()
        self.data_u_p.clear()
        self.data_u_i.clear()
        self.data_u_d.clear()
        self.canvas.draw_idle()


