from pypst import Image, utils


def test_flat_mapping():
    obj = dict(foo='"bar"', quux='"corge"', qux=None, baz=Image("image.png"))
    assert (
        utils.render(obj)
        == '(foo: "bar", quux: "corge", qux: none, baz: image("image.png"))'
    )


def test_nested_mapping():
    obj = dict(foo=dict(bar='"quux"', qux=None, baz=Image("image.png")))
    assert (
        utils.render(obj) == '(foo: (bar: "quux", qux: none, baz: image("image.png")))'
    )


def test_flat_sequence():
    obj = ('"foo"', "bar", 2, Image("image.png"), None)
    assert utils.render(obj) == '("foo", bar, 2, image("image.png"), none)'


def test_nested_seq():
    obj = ('"foo"', "bar", (2, Image("image.png")), None)
    assert utils.render(obj) == '("foo", bar, (2, image("image.png")), none)'
