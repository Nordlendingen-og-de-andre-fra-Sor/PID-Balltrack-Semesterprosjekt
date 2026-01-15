# app_screen.py
import tkinter as tk
import time

from V8_BALLTRACK.gui.widgets.control.setpoint_widget import SetpointWidget
from V8_BALLTRACK.gui.widgets.control.control_widget import ControlWidget
from V8_BALLTRACK.gui.widgets.control.servo_widget import ServoWidget

from V8_BALLTRACK.gui.widgets.pid.pid_widget import PIDWidget

from V8_BALLTRACK.gui.widgets.monitoring.plot_widget import PlotWidget
from V8_BALLTRACK.gui.widgets.monitoring.log_widget import LogWidget
from V8_BALLTRACK.gui.widgets.monitoring.footer_widget import FooterWidget
from V8_BALLTRACK.gui.widgets.monitoring.balltrack_visual_widget import BalltrackVisualWidget



class BalltrackApp:
    """
    Screen/HMI:
    - Plasserer faceplates/widgets
    - Binder dem mot tags (GuiTags) via bind()
    - Oppdaterer visning basert på tags.get_status()
    """

    def __init__(self, root: tk.Tk, tags):
        self.root = root
        self.tags = tags

        self._last_t = time.monotonic()


        self._configure_root()
        self._build_layout()
        self._bind_widgets()

        # UI refresh + cyclic controller update

        self._ui_poll()

    def _configure_root(self):
        self.root.title("Balltrack V8")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

    def _build_layout(self):
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        # TOPP
        self.setpoint = SetpointWidget(main)
        self.setpoint.pack(fill="x", padx=8, pady=6)

        # MIDT
        mid = tk.Frame(main)
        mid.pack(fill="both", expand=True)

        left = tk.Frame(mid)
        left.pack(side="left", fill="y", padx=8, pady=6)

        center = tk.Frame(mid)
        center.pack(side="left", fill="both", expand=True, padx=8, pady=6)

        right = tk.Frame(mid)
        right.pack(side="right", fill="both", padx=8, pady=6)

        self.pid = PIDWidget(left)
        self.pid.pack(fill="x", pady=6)

        self.control = ControlWidget(left)
        self.control.pack(fill="x", pady=6)

        self.servo = ServoWidget(left)
        self.servo.pack(fill="x", pady=6)

        self.visual = BalltrackVisualWidget(center)
        self.visual.pack(fill="both", expand=True)

        self.plot = PlotWidget(right)
        self.plot.pack(fill="both", expand=True)

        self.log = LogWidget(right)
        self.log.pack(fill="both", expand=True, pady=6)

        # FOOTER
        self.footer = FooterWidget(main)
        self.footer.pack(fill="x", padx=8, pady=6)

    def _bind_widgets(self):
        for w in (self.setpoint, self.pid, self.control, self.servo, self.visual, self.plot, self.log, self.footer):
            if hasattr(w, "bind"):
                w.bind(self.tags)


    def _ui_poll(self):
        # NYTT: cyclic update av controller via tags
        now = time.monotonic()
        dt = now - self._last_t
        self._last_t = now

        # clamp dt for stabil oppførsel
        dt = max(0.0, min(0.2, dt))

        if hasattr(self.tags, "update"):
            self.tags.update(dt)

        status = {}
        if hasattr(self.tags, "get_status"):
            status = self.tags.get_status() or {}

        # Plot: gi den feltene den forventer
        if hasattr(self.plot, "update_plot"):
            self.plot.update_plot(
                status.get("setpoint", 0.0),
                status.get("pos", 0.0),
                status.get("u", 0.0),
                status.get("P", 0.0),
                status.get("I", 0.0),
                status.get("D", 0.0),
            )

        # Footer: unpack dict
        if hasattr(self.footer, "update_status"):
            self.footer.update_status(
                raw=status.get("raw", "---"),
                pos=status.get("pos", "---"),
                sp=status.get("setpoint", "---"),
                u=status.get("u", "---"),
                servo_us=status.get("pulse_us", "---"),
                mode=status.get("mode", "---"),
            )

        if hasattr(self.visual, "update_status"):
            self.visual.update_status(status)

        self.root.after(50, self._ui_poll)  # 20 Hz GUI refresh


def run_app(tags):
    root = tk.Tk()
    BalltrackApp(root, tags)
    root.mainloop()