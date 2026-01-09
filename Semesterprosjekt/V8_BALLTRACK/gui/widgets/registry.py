# V8_BALLTRACK/gui/widgets/registry.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Type, Optional
import importlib
import pkgutil

@dataclass(frozen=True)
class WidgetSpec:
    key: str
    title: str
    cls: Type

_REGISTRY: Dict[str, WidgetSpec] = {}

def register_widget(key: str, title: Optional[str] = None) -> Callable[[Type], Type]:
    """
    Dekoratør for å registrere en widget/faceplate.
    Bruk:
        @register_widget("control", "Preview – ControlWidget")
        class ControlWidget(BaseWidget): ...
    """
    def deco(widget_cls: Type) -> Type:
        spec = WidgetSpec(
            key=key,
            title=title or f"Preview – {widget_cls.__name__}",
            cls=widget_cls,
        )
        if key in _REGISTRY:
            raise KeyError(f"Widget key '{key}' er allerede registrert av {_REGISTRY[key].cls}")
        _REGISTRY[key] = spec
        return widget_cls
    return deco

def get_registry() -> Dict[str, WidgetSpec]:
    return dict(_REGISTRY)

def get_spec(key: str) -> WidgetSpec:
    return _REGISTRY[key]

def autodiscover_widgets():
    """
    Importerer alle moduler under V8_BALLTRACK.gui.widgets.* slik at dekoratørene kjøres.
    Kall denne én gang i preview/test-program.
    """
    base_pkg = "V8_BALLTRACK.gui.widgets"
    pkg = importlib.import_module(base_pkg)

    for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        # m.name er full modulsti
        importlib.import_module(m.name)
