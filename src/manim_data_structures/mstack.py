from __future__ import annotations

import copy
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    SupportsIndex,
    TypeVar,
    Union,
)

import numpy as np

from manim_data_structures import LinearCollection

if TYPE_CHECKING:
    from _typeshed import Self, SupportsRichComparison
else:
    Self = Any
    SupportsRichComparison = Any

from manim import BLACK, ORIGIN, OUT, UP, Integer, Mobject, Square

_V = TypeVar("_V")
_D = TypeVar("_D", bound=Mobject)
_C = TypeVar("_C", bound=Mobject)


class Stack(LinearCollection, Generic[_V, _D, _C]):
    """A Stack is a LinearCollection that is ordered from top to bottom.

    Parameters
    ----------
    __data_type
        The type of the data to be displayed in the stack.
    __container_type
        The type of the container to be displayed in the stack.
    __data_kwargs
        The kwargs to be passed to the data.
    __container_kwargs
        The kwargs to be passed to the container.
    kwargs
        The kwargs to be passed to the stack.
    """

    def __init__(
        self,
        __data_type: type[_D] = Integer,
        __container_type: type[_C] = Square,
        __data_kwargs: dict[str, Any] = {},
        __container_kwargs: dict[str, Any] = {"fill_color": BLACK, "fill_opacity": 1},
        __arrangement={"direction": UP, "buff": 0.0, "center": False},
        **kwargs,
    ):

        super().__init__(
            (),
            lambda v: __data_type(v, **__data_kwargs),
            lambda: __container_type(**__container_kwargs),
            None,
            __arrangement,
            **kwargs,
        )

    def pop(self):
        return super().pop(-1)

    def peek(self):
        return super().__getitem__(-1)

    def push(self, value: _V):
        super().append(value)


if __name__ == "__main__":
    from manim import *

    class StackTest(Scene):
        def construct(self):
            stk = Stack()
            text = Text("l = stack()").to_edge(UP)
            self.wait()
            self.play(Write(text))
            self.play(Create(stk))
            self.wait()
            stk.push(6)
            self.wait()
            stk.push(12)
            self.wait()
            stk.push(7)
            self.wait()
            print(stk.peek())
            print(stk.pop())
            self.wait()

    config.preview = True
    config.render = "cairo"
    config.quality = "low_quality"
    StackTest().render(preview=True)
