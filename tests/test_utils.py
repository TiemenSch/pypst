import pytest
from pypst import Image, utils
from datetime import date, datetime, timedelta


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


def test_date():
    obj = date(2024, 12, 18)
    assert utils.render(obj) == "#datetime(year: 2024, month: 12, day: 18)"


def test_datetime():
    obj = datetime(2024, 12, 18, 15, 34, 12)
    assert (
        utils.render(obj)
        == "#datetime(year: 2024, month: 12, day: 18, hour: 15, minute: 34, second: 12)"
    )


def test_timedelta():
    obj = timedelta(days=3, seconds=4)
    assert utils.render(obj) == "#duration(seconds: 4, days: 3)"
    obj = timedelta(
        days=3, seconds=4, microseconds=7e5
    )  # millis are not supported in Typst, but we round them to seconds.
    assert utils.render(obj) == "#duration(seconds: 5, days: 3)"


@pytest.mark.integration
def test_date_compile(compile_rendered):
    obj = date(2024, 12, 18)
    assert compile_rendered(obj)


@pytest.mark.integration
def test_datetime_compile(compile_rendered):
    obj = datetime(2024, 12, 18, 15, 34, 12)
    compile_rendered(obj)


@pytest.mark.integration
def test_timedelta_compile(compile_rendered):
    obj = timedelta(
        days=3, seconds=4, microseconds=7e5
    )  # millis are not supported in Typst, but we round them to seconds.
    compile_rendered(obj)
