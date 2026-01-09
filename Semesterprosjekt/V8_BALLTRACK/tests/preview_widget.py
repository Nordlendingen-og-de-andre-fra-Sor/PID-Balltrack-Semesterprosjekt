# V8_BALLTRACK/tests/preview_widget.py
import sys
import tkinter as tk

from V8_BALLTRACK.tests.mock_gui_tags import MockGuiTags
from V8_BALLTRACK.gui.widgets.registry import autodiscover_widgets, get_registry, get_spec

def main():
    autodiscover_widgets()
    registry = get_registry()

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("Bruk:")
        print("  python -m V8_BALLTRACK.tests.preview_widget <widget_key>")
        print("Tilgjengelig:")
        for k in sorted(registry.keys()):
            print(f"  - {k:10s}  ({registry[k].cls.__name__})")
        raise SystemExit(0)

    key = sys.argv[1]
    if key not in registry:
        print(f"Ukjent widget_key: {key}")
        print("Tilgjengelig:", ", ".join(sorted(registry.keys())))
        raise SystemExit(2)

    spec = get_spec(key)
    tags = MockGuiTags()

    root = tk.Tk()
    root.title(spec.title)

    w = spec.cls(root)
    w.pack(fill="both", expand=True, padx=20, pady=20)

    if hasattr(w, "bind"):
        w.bind(tags)

    # jevn statusoppdatering for monitoring-widgets
    def tick():
        _ = tags.get_status()
        root.after(50, tick)

    tick()
    root.mainloop()

if __name__ == "__main__":
    main()
