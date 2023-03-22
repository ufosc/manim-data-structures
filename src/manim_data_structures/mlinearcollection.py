from __future__ import annotations

import copy
from typing import Any, Callable, Iterable, List, SupportsIndex, Union

import numpy as np
from manim import ORIGIN, RIGHT, Integer, Mobject, Square, VMobject


class LinearCollection(VMobject):
    """
    A drop-in replacement for a Python list that supports animating operations.
    """

    __datas: List[Mobject]
    __containers: List[Mobject]
    __data_template: Callable[[Any], Mobject]
    __container_template: Callable[[], Mobject]
    __delimiter: Mobject
    __arrangement: dict

    def __init__(
        self,
        data: Iterable,
        data_template=Integer,
        container_template=Square,
        delimiter=None,
        arrangement={"direction": RIGHT, "buff": 0.0},
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__datas = []
        self.__containers = []
        self.__data_template = data_template
        self.__container_template = lambda data: container_template().add(
            data.move_to(ORIGIN)
        )
        self.__delimiter = delimiter
        self.__arrangement = arrangement

        for value in data:
            self.append(value)

        self.updaters.append(LinearCollection.__update)

    @classmethod
    def __update(cls, mobject, dt=0):
        # Only rearrange if we need to
        if mobject.__rearrange:
            mobject.arrange(**mobject.__arrangement)
            mobject.__rearrange = False

    # Python list style methods
    def append(self, value: Any) -> LinearCollection:
        return self.insert(len(self), value)

    def extend(self, values: Iterable) -> LinearCollection:
        for value in values:
            self.append(value)

    def insert(self, index, value) -> LinearCollection:
        self.__datas.insert(index, self.__data_template(value))
        self.__containers.insert(index, self.__container_template(self.__datas[index]))
        if self.__delimiter is not None:
            super().insert(2 * index, self.__delimiter.copy())
        super().insert(2 * index, self.__containers[-1])

        # Flag for rearrangement
        self.__rearrange = True
        return self

    def remove(self, value: Any) -> LinearCollection:
        index = self.index(value)
        self.pop(index)
        self.__rearrange = True
        return self

    def pop(self, index=-1) -> Any:
        self.__datas.pop(index)
        self.__containers.pop(index)
        self.submobjects.pop(2 * index)
        self.submobjects.pop(2 * index)
        self.__rearrange = True
        pass

    def clear(self) -> LinearCollection:
        self.__datas.clear()
        self.__containers.clear()
        self.submobjects.clear()
        self.__rearrange = True
        return self

    def index(self, value: Any, start=0, end=None) -> int:
        for i, data in self.__datas[start:end]:
            if data.get_value() == value:
                return i

    def count(self, value: Any) -> int:
        count = 0
        for i, data in self.__datas:
            if data.get_value() == value:
                count += 1
        return count

    def sort(self, key=None, reverse=False) -> LinearCollection:
        # TODO #
        raise NotImplementedError("Sorting is not yet implemented")
        self.__rearrange = True
        return self

    def reverse(self) -> LinearCollection:
        # TODO #
        raise NotImplementedError("Reversing is not yet implemented")
        self.__rearrange = True
        return self

    # Comparison Operators
    def __lt__(self, rhs):
        for lhs_data, rhs_data in zip(self, rhs):
            if lhs_data != rhs_data:
                return lhs_data < rhs_data
        return len(self) < len(rhs)

    def __le__(self, rhs):
        for lhs_data, rhs_data in zip(self, rhs):
            if lhs_data != rhs_data:
                return lhs_data < rhs_data
        return len(self) <= len(rhs)

    def __eq__(self, rhs):
        if type(rhs) != LinearCollection or len(self) != len(rhs):
            return False
        return all(lhs_data == rhs_data for lhs_data, rhs_data in zip(self, rhs))

    def __ne__(self, rhs: LinearCollection):
        return not self.__eq__(rhs)

    def __gt__(self, rhs: Union[Iterable, LinearCollection]):
        for lhs_data, rhs_data in zip(self, rhs):
            if lhs_data != rhs_data:
                return lhs_data > rhs_data
        return len(self) > len(rhs)

    def __ge__(self, rhs: LinearCollection):
        for lhs_data, rhs_data in zip(self, rhs):
            if lhs_data != rhs_data:
                return lhs_data > rhs_data
        return len(self) >= len(rhs)

    # Iteration and indexing proxy to the values of __datas
    def __len__(self) -> int:
        return self.__datas.__len__()

    def __getitem__(self, key: SupportsIndex) -> Any:
        # TODO support slicing #
        return self.__datas.__getitem__(key).get_value()

    def __setitem__(self, key: SupportsIndex, value: Any) -> None:
        # TODO support slicing #
        return self.__datas.__getitem__(key).set_value(value)

    def __delitem__(self, key: SupportsIndex) -> None:
        # TODO support slicing #
        self.__datas.__delitem__(key)
        self.__containers.__delitem__(key)
        self.__rearrange = True

    def __iter__(self):
        # Initialize a Data iterator when we start iterating
        self.__iter__data = iter(self.__datas)
        return self

    def __next__(self):
        try:
            # Return the value of the next Data in the iterator
            return next(self.__iter__data).get_value()
        except StopIteration as e:
            # Clean up the iterator when we're done
            del self.__iter__data
            raise e

    # Concatenation
    def __iadd__(self, rhs: Union[Iterable, LinearCollection]):
        if not isinstance(rhs, LinearCollection):
            raise NotImplementedError(
                "unsupported operand type(s) for +: 'LinearCollection' and '{}'".format(
                    type(rhs)
                )
            )

        for container in rhs.submobjects:
            container_copy = copy.copy(container)
            self.__datas.append(container_copy.submobjects[0])
            self.__containers.append(container_copy)
            self.add(container_copy)
            if self.__delimiter is not None:
                self.add(self.__delimiter.copy())

        self.__rearrange = True
        return self

    def __add__(self, rhs: Union[Iterable, LinearCollection]):
        self_copy = copy.copy(self)
        self_copy += rhs
        return self_copy

    def __imul__(self, rhs: SupportsIndex):
        if type(rhs) is not int:
            raise NotImplementedError(
                "unsupported operand type(s) for *: 'LinearCollection' and '{}'".format(
                    type(rhs)
                )
            )

        self_copy = copy.copy(self)
        for _ in range(rhs):
            self += self_copy

        self.__rearrange = True
        return self

    def __mul__(self, rhs: SupportsIndex):
        self_copy = copy.copy(self)
        self_copy *= rhs
        return self_copy

    def __rmul(self, lhs: SupportsIndex):
        return self.__mul__(lhs)
