"""Tests for the Attribute class."""


from stransi.attribute import Attribute


def test_whether_attribute_is_on_or_off():
    """Test whether the Attribute class is working correctly."""
    assert Attribute.NORMAL.is_on()
    assert Attribute.BOLD.is_on()
    assert Attribute.DIM.is_on()
    assert Attribute.ITALIC.is_on()
    assert Attribute.UNDERLINE.is_on()
    assert Attribute.BLINK.is_on()
    assert Attribute.REVERSE.is_on()
    assert Attribute.HIDDEN.is_on()

    assert Attribute.NEITHER_BOLD_NOR_DIM.is_off()
    assert Attribute.NOT_ITALIC.is_off()
    assert Attribute.NOT_UNDERLINE.is_off()
    assert Attribute.NOT_BLINK.is_off()
    assert Attribute.NOT_REVERSE.is_off()
    assert Attribute.NOT_HIDDEN.is_off()
