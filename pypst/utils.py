from typing import Sequence, Mapping, Iterable, Any

from pypst.renderable import Renderable

BuiltIn = (
    bool
    | int
    | float
    | str
    | Sequence[Renderable | "BuiltIn"]
    | Mapping[str, Renderable | "BuiltIn"]
)


def render(obj: Renderable | BuiltIn) -> str:
    """
    Render renderable objects using their `render` method
    or use the `render_type` utility to render built-in Python types.
    """
    if isinstance(obj, Renderable):
        rendered = obj.render()
    else:
        rendered = render_type(obj)

    return rendered


def render_type(arg: BuiltIn) -> str:
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


def render_mapping(arg: Mapping[str, Renderable | BuiltIn]) -> str:
    """
    Render a mapping from string to any object supported by `render`.
    """
    return render_sequence(f"{k}: {render(v).lstrip("#")}" for k, v in arg.items())


def render_sequence(arg: Iterable[Renderable | BuiltIn]) -> str:
    """
    Render a sequence of any object supported by `render`.
    """
    return f"({', '.join(render(a).lstrip("#") for a in arg)})"
