"""Contains enums used throughout the package."""

from enum import Enum


class MArrayElementComp(Enum):
    """Refers to individual component :class:`~manim.mobject.mobject.Mobject`\0s of :class:`~.m_array.MArrayElement`."""
    def __init__(self):
        self.BODY = 0
        """:class:`~manim.mobject.geometry.polygram.Square` that represents the body."""

        self.VALUE = 1
        """:class:`~manim.mobject.text.text_mobject.Text` that represents the value."""

        self.INDEX = 2
        """:class:`~manim.mobject.text.text_mobject.Text` that represents the index."""

        self.LABEL = 3
        """:class:`~manim.mobject.text.text_mobject.Text` that represents the label."""
    def get_body(self):
        return self.BODY
    def get_value(self):
        return self.VALUE
    def get_index(self):
        return self.INDEX
    def get_label(self):
        return self.LABEL
    def set_body(self, body):
        self.BODY = body
    def set_value(self, value):
        self.VALUE = value
    def set_index(self, index):
        self.INDEX = index
    def set_label(self, label):
        self.LABEL = label

class MArrayDirection(Enum):
    """Serves as the direction for :class:`~.m_array.MArray`."""

    UP = 0
    """Upward direction."""

    DOWN = 1
    """Downward direction."""

    RIGHT = 2
    """Rightward direction."""

    LEFT = 3
    """Leftward direction."""
