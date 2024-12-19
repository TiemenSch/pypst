from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, fields
from datetime import date, datetime, timedelta
from typing import Any

from pypst.renderable import Renderable


def render(
    obj: Renderable
    | bool
    | int
    | float
    | str
    | Sequence[Any]
    | Mapping[str, Any]
    | date
    | datetime
    | timedelta
    | None,
) -> str:
    """
    Render renderable objects using their `render` method
    or use the `render_type` utility to render built-in Python types.
    """
    if isinstance(obj, Renderable):
        rendered = obj.render()
    else:
        rendered = render_type(obj)

    return rendered


def render_code(
    obj: Renderable
    | bool
    | int
    | float
    | str
    | Sequence[Any]
    | Mapping[str, Any]
    | date
    | datetime
    | timedelta
    | None,
) -> str:
    """
    Render renderable objects using the `render` method
    and strip any `#` code-mode prefixes.
    """
    return render(obj).lstrip("#")


def render_type(
    arg: bool
    | int
    | float
    | str
    | Sequence[Any]
    | Mapping[str, Any]
    | date
    | datetime
    | timedelta
    | None,
) -> str:
    """
    Render different built-in Python types.
    """
    if arg is None:
        rendered_arg = "none"
    elif isinstance(arg, bool):
        rendered_arg = str(arg).lower()
    elif isinstance(arg, int | float):
        rendered_arg = str(arg)
    elif isinstance(arg, str):
        rendered_arg = arg
    elif isinstance(arg, Sequence):
        rendered_arg = render_sequence(arg)
    elif isinstance(arg, Mapping):
        rendered_arg = render_mapping(arg)
    elif isinstance(arg, date):
        rendered_arg = render_datetime(arg)
    elif isinstance(arg, timedelta):
        rendered_arg = render_timedelta(arg)
    else:
        raise ValueError(f"Invalid argument type: {type(arg)}")

    return rendered_arg


def render_mapping(arg: Mapping[str, Any]) -> str:
    """
    Render a mapping from string to any object supported by `render`.
    """
    return render_sequence(f"{k}: {render_code(v)}" for (k, v) in arg.items())


def render_sequence(arg: Iterable[Any]) -> str:
    """
    Render a sequence of any object supported by `render`.
    """
    return f"({', '.join(render_code(a) for a in arg)})"


def render_datetime(arg: date | datetime) -> str:
    """
    Render a Python `datetime.date` into a call to the Typst datetime function.
    """
    obj = {
        name: getattr(arg, name)
        for name in ["year", "month", "day", "hour", "minute", "second"]
        if hasattr(arg, name)
    }
    return f"#datetime{render_mapping(obj)}"


def render_timedelta(arg: timedelta) -> str:
    """
    Render a Python `datetime.timedelta` into a call to the Typst duration function.
    """
    obj = {
        name: getattr(arg, name)
        for name in [
            "microseconds",
            "seconds",
            "days",
        ]
        if hasattr(arg, name)
    }
    obj["seconds"] = obj["seconds"] + round(obj.pop("milliseconds") / 1e6)
    return f"#duration{render_mapping(obj)}"


@dataclass
class RenderDataclass:
    """
    Helper class to render Python dataclasses by iterating over its fields
    as if it were a dictionary.

    Inherit from `RenderDataclass` to inherit the render method
    and stick it on your dataclass.
    """

    def render(self):
        """
        Dataclass rendering using fields iteration
        and recursively using Pypst rendering.
        """
        return render_mapping(
            {field.name: render(getattr(self, field.name)) for field in fields(self)}
        )
