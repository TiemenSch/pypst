from pypst.renderable import Plain, Renderable


def test_renderable():
    class Foo:
        pass

    class Bar:
        def render() -> str:
            pass

    assert not issubclass(Foo, Renderable)
    assert issubclass(Bar, Renderable)
    assert not isinstance(Foo(), Renderable)
    assert isinstance(Bar(), Renderable)


def test_plain():
    plain = Plain("Lorem ipsum dolor sit amet.")
    assert plain.render() == "Lorem ipsum dolor sit amet."
