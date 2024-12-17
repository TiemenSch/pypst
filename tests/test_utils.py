from pypst import Image, utils


def test_flat_mapping():
    obj = dict(foo='"bar"', quux='"corge"', baz=Image("image.png"))
    assert utils.render(obj) == '(foo: "bar", quux: "corge", baz: image("image.png"))'


def test_nested_mapping():
    obj = dict(foo=dict(bar='"quux"', baz=Image("image.png")))
    assert utils.render(obj) == '(foo: (bar: "quux", baz: image("image.png")))'


def test_flat_sequence():
    obj = ('"foo"', "bar", 2, Image("image.png"))
    assert utils.render(obj) == '("foo", bar, 2, image("image.png"))'


def test_nested_seq():
    obj = ('"foo"', "bar", (2, Image("image.png")))
    assert utils.render(obj) == '("foo", bar, (2, image("image.png")))'
