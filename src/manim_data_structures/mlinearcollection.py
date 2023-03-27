from __future__ import annotations

import copy
from typing import Any, Callable, Iterable, List, SupportsIndex, Union

import numpy as np
from manim import ORIGIN, RIGHT, Integer, Mobject, Square, VMobject


class LinearCollection(VMobject):
    """
    A drop-in replacement for a Python list that supports animating operations.
    """

    __values: List[Any]
    __datas: List[Mobject]
    __containers: List[Mobject]
    __data_constructor: Callable[[Any], Mobject]
    __container_constructor: Callable[[], Mobject]
    __delimiter: Mobject
    __arrangement: dict
    __rearrange: bool

    def __init__(
        self,
        data: Iterable[Any] = (),
        data_constructor: Callable[[Any], Mobject] = Integer,
        container_constructor: Callable[[], Mobject] = Square,
        delimiter=None,
        arrangement={"direction": RIGHT, "buff": 0.0},
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__values = []
        self.__datas = []
        self.__containers = []
        self.__data_constructor = data_constructor
        self.__container_constructor = lambda data: container_constructor().add(
            data.move_to(ORIGIN)
        )
        self.__delimiter = delimiter
        self.__arrangement = arrangement
        self.__rearrange = False

        self.extend(data)

        self.updaters.append(LinearCollection.__update)

    @classmethod
    def __update(cls, lc: LinearCollection, dt=0):
        # Only rearrange if we need to
        if lc.__rearrange:
            lc.arrange(**lc.__arrangement)
            lc.__rearrange = False

    def __submobject_index(self, index):
        index = index if self.__delimiter is None else 2 * index
        return index if index >= 0 else index + 1

    def __rebuild_submobjects(self):
        self.submobjects.clear()
        for container in self.__containers:
            self.submobjects.append(container)
            if (
                self.__delimiter is not None
                and len(self.submobjects) < 2 * len(self) - 1
            ):
                self.submobjects.append(self.__delimiter.copy())

        self.__rearrange = True
        return self

    # Python list style methods
    def append(self, value: Any) -> LinearCollection:
        return self.insert(len(self), value)

    def extend(self, values: Iterable[Any]) -> LinearCollection:
        for value in values:
            self.append(value)

    def insert(self, index, value) -> LinearCollection:
        self.__values.insert(index, value)
        new_data = self.__data_constructor(value)
        self.__datas.insert(index, new_data)
        new_container = self.__container_constructor(new_data)
        self.__containers.insert(index, new_container)

        submobject_index = self.__submobject_index(index)
        if self.__delimiter is not None and len(self.submobjects) > 0:
            super().insert(submobject_index, self.__delimiter.copy())
        if submobject_index < 0:
            submobject_index -= 1
        super().insert(submobject_index, new_container)

        # Flag for rearrangement
        self.__rearrange = True
        return self

    def remove(self, value: Any) -> LinearCollection:
        index = self.index(value)
        self.__delitem__(index)

        self.__rearrange = True
        return self

    def pop(self, index=-1) -> Any:
        value = self.__values[index]
        del self[index]

        self.__rearrange = True
        return value

    def clear(self) -> LinearCollection:
        self.__values.clear()
        self.__datas.clear()
        self.__containers.clear()
        self.submobjects.clear()

        return self

    def index(self, *args) -> int:
        return self.__values.index(*args)

    def count(self, value: Any) -> int:
        return self.__values.count(value)

    def sort(self, key=lambda x: x, reverse=False) -> LinearCollection:
        if len(self) == 0:
            return

        self.__values, self.__datas, self.__containers = zip(
            *sorted(
                zip(self.__values, self.__datas, self.__containers),
                key=(lambda x: key(x[0])),
                reverse=reverse,
            )
        )
        self.__rebuild_submobjects()

        return self

    def reverse(self) -> LinearCollection:
        self.__values.reverse()
        self.__datas.reverse()
        self.__containers.reverse()
        self.submobjects.reverse()

        self.__rearrange = True
        return self

    # Comparison Operators
    def __lt__(self, rhs):
        if isinstance(rhs, LinearCollection):
            return self.__values.__lt__(rhs.__values)
        if isinstance(rhs, list):
            return self.__values.__lt__(rhs)

        raise TypeError(
            f"'<' not supported between instances of 'LinearCollection' and '{type(rhs)}'"
        )

    def __le__(self, rhs):
        if isinstance(rhs, LinearCollection):
            return self.__values.__le__(rhs.__values)
        if isinstance(rhs, list):
            return self.__values.__le__(rhs)

        raise TypeError(
            f"'<=' not supported between instances of 'LinearCollection' and '{type(rhs)}'"
        )

    def __eq__(self, rhs):
        return not self.__ne__(rhs)

    def __ne__(self, rhs: LinearCollection):
        if isinstance(rhs, LinearCollection):
            return self.__values.__ne__(rhs.__values)
        if isinstance(rhs, list):
            return self.__values.__ne__(rhs)

        return True

    def __gt__(self, rhs: Union[Iterable, LinearCollection]):
        if isinstance(rhs, LinearCollection):
            return self.__values.__gt__(rhs.__values)
        if isinstance(rhs, list):
            return self.__values.__gt__(rhs)

        raise TypeError(
            f"'>' not supported between instances of 'LinearCollection' and '{type(rhs)}'"
        )

    def __ge__(self, rhs: LinearCollection):
        if isinstance(rhs, LinearCollection):
            return self.__values.__ge__(rhs.__values)
        if isinstance(rhs, list):
            return self.__values.__ge__(rhs)

        raise TypeError(
            f"'>=' not supported between instances of 'LinearCollection' and '{type(rhs)}'"
        )

    def __len__(self) -> int:
        return self.__values.__len__()

    def __getitem__(self, index: SupportsIndex) -> Any:
        return self.__values.__getitem__(index)

    def __setitem__(self, index: SupportsIndex, value: Any) -> None:
        self.__values.__setitem__(index, value)
        try:
            self.__datas[index] = (self.__data_constructor(val) for val in value)
        except TypeError:
            self.__datas[index] = self.__data_constructor(value)

    def __delitem__(self, index: SupportsIndex) -> None:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(f"LinearCollection index out of range: {index}")

        submobject_index = self.__submobject_index(index)
        self.submobjects.__delitem__(submobject_index)
        if self.__delimiter is not None and len(self.submobjects) > 0:
            if index != -1 and index != len(self) - 1:
                self.submobjects.__delitem__(submobject_index)
            else:
                self.submobjects.__delitem__(submobject_index - 1)

        self.__values.__delitem__(index)
        self.__datas.__delitem__(index)
        self.__containers.__delitem__(index)
        self.__rearrange = True

    def __iter__(self):
        return self.__values.__iter__()

    # Concatenation
    def __iadd__(self, rhs: Iterable) -> LinearCollection:
        self.extend(rhs)
        return self

    def __add__(self, rhs: Union[Iterable, LinearCollection]):
        self_copy = copy.copy(self)
        self_copy += rhs
        return self_copy

    def __imul__(self, rhs: SupportsIndex):
        if not hasattr(rhs, "__index__"):
            raise NotImplementedError(
                "unsupported operand type(s) for *: 'LinearCollection' and '{}'".format(
                    type(rhs)
                )
            )

        num_repeats = rhs.__index__() - 1
        self_copy = self.copy()
        for _ in range(num_repeats):
            self += self_copy

        self.__rearrange = True
        return self

    def __mul__(self, rhs: SupportsIndex):
        self_copy = copy.copy(self)
        self_copy *= rhs
        return self_copy

    def __rmul__(self, lhs: SupportsIndex):
        return self.__mul__(lhs)

    def __copy__(self):
        self_copy = super().copy()
        self_copy.__values = self.__values.copy()
        self_copy.__containers = copy.deepcopy(self.__containers)
        self_copy.__datas = [
            container.submobjects[0] for container in self_copy.__containers
        ]
        self_copy.__data_constructor = copy.copy(self.__data_constructor)
        self_copy.__container_constructor = copy.copy(self.__container_constructor)
        self_copy.__delimiter = self.__delimiter
        self_copy.__arrangement = self.__arrangement
        self_copy.__rearrange = self.__rearrange
        self_copy.__rebuild_submobjects()

        return self_copy

    def copy(self):
        return self.__copy__()
