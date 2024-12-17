from collections.abc import Iterable, Mapping, Sequence
from typing import Any
from pypst.renderable import Renderable


def render(
    obj: Renderable | bool | int | float | str | Sequence[Any] | Mapping[str, Any],
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
    obj: Renderable | bool | int | float | str | Sequence[Any] | Mapping[str, Any],
) -> str:
    """
    Render renderable objects using the `render` method
    and strip any `#` code-mode prefixes.
    """
    return render(obj).lstrip("#")


def render_type(
    arg: bool | int | float | str | Sequence[Any] | Mapping[str, Any],
) -> str:
    """
    Render different built-in Python types.
    """
    if isinstance(arg, bool):
        rendered_arg = str(arg).lower()
    elif isinstance(arg, int | float):
        rendered_arg = str(arg)
    elif isinstance(arg, str):
        rendered_arg = arg
    elif isinstance(arg, Sequence):
        rendered_arg = render_sequence(arg)
    elif isinstance(arg, Mapping):
        rendered_arg = render_mapping(arg)
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
