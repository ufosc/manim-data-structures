from __future__ import annotations

import copy
import sys
from typing import Any, Callable, Generic, Iterable, Self, SupportsIndex, TypeVar, Union

import numpy as np
from _typeshed import SupportsRichComparison, SupportsRichComparisonT
from manim import ORIGIN, RIGHT, Integer, Mobject, Square, VMobject

_V = TypeVar("_V")
_D = TypeVar("_D", Mobject)
_C = TypeVar("_C", Mobject)
_Delimiter = TypeVar("_Delimiter", Mobject)


class LinearCollection(
    VMobject,
    Generic[_V, _D, _C, _Delimiter],
):

    __values: list[_V]
    __datas: list[_D]
    __containers: list[_C]
    __data_constructor: Callable[[_V], _D]
    __container_constructor: Callable[[], _C]
    __delimiter: _Delimiter
    __arrangement: dict
    __rearrange: bool

    def __init__(
        self,
        __values: Iterable[_V] = (),
        __data_constructor: Callable[[_V], _D] = Integer,
        __container_constructor: Callable[[], _C] = Square,
        __delimiter: _Delimiter = None,
        __arrangement={"direction": RIGHT, "buff": 0.0},
        *args,
        **kwargs,
    ):
        """Constructs a new LinearCollection.

        Parameters
        ----------
        __values : Iterable[_V], optional
            the iterable of values to convert, by default ()
        __data_constructor : Callable[[_V], _D], optional
            a callable that converts values to an Mobject representation, by default Integer
        __container_constructor : Callable[[], _C], optional
            a callable that constructs a container, by default Square
        __delimiter : _Delimiter, optional
            an optional delimiter that is placed between containers, by default None
        __arrangement : dict, optional
            a dict of kwargs that is passed to self.arrange, by default {"direction": RIGHT, "buff": 0.0}
        """
        super().__init__(*args, **kwargs)

        self.__values = []
        self.__datas = []
        self.__containers = []
        self.__data_constructor = __data_constructor
        self.__container_constructor = lambda data: __container_constructor().add(
            data.move_to(ORIGIN)
        )
        self.__delimiter = __delimiter
        self.__arrangement = __arrangement
        self.__rearrange = False

        self.extend(__values)

        self.updaters.append(LinearCollection.__update)

    @classmethod
    def __update(cls, lc: Self, dt=0):
        """An updater that is applied to each LinearCollection before every frame.

        Parameters
        ----------
        lc : Self
            the target to format
        dt : int, optional
            the time that has passed since the last update, by default 0
        """
        # Only rearrange if we need to
        if lc.__rearrange:
            lc.arrange(**lc.__arrangement)
            lc.__rearrange = False

    def __submobject_index(self, __index: int) -> int:
        """Returns the index in submobjects of the given container index.

        Parameters
        ----------
        __index : int
            the external index of the value

        Returns
        -------
        int
            the index of the container in submobjects
        """
        __index = __index if self.__delimiter is None else 2 * __index
        return __index if __index >= 0 else __index + 1

    def __rebuild_submobjects(self):
        """Rebuilds the submobject list to obey the order of self.__containers."""
        self.submobjects.clear()
        for container in self.__containers:
            self.submobjects.append(container)
            if (
                self.__delimiter is not None
                and len(self.submobjects) < 2 * len(self) - 1
            ):
                self.submobjects.append(self.__delimiter.copy())

        self.__rearrange = True

    # Python list style methods
    def append(self, __value: _V) -> Self:
        """Appends the value.

        Parameters
        ----------
        __value : _V
            the value to append

        Returns
        -------
        Self
            a reference to self
        """
        return self.insert(len(self), __value)

    def extend(self, __iterable: Iterable[_V]) -> Self:
        """Appends all items from the iterable.

        Parameters
        ----------
        __iterable : Iterable[_V]
            an iterable of values to append

        Returns
        -------
        Self
            a reference to self
        """
        for value in __iterable:
            self.append(value)

    def insert(self, __index: SupportsIndex, __value: _V) -> Self:
        self.__values.insert(__index, __value)
        new_data = self.__data_constructor(__value)
        self.__datas.insert(__index, new_data)
        new_container = self.__container_constructor(new_data)
        self.__containers.insert(__index, new_container)

        submobject_index = self.__submobject_index(__index.__index__())
        if self.__delimiter is not None and len(self.submobjects) > 0:
            super().insert(submobject_index, self.__delimiter.copy())
        if submobject_index < 0:
            submobject_index -= 1
        super().insert(submobject_index, new_container)

        # Flag for rearrangement
        self.__rearrange = True
        return self

    def remove(self, __value: _V) -> Self:
        """Removes the first value that is equal to __value.

        Parameters
        ----------
        __value : _V
            the value to remove

        Returns
        -------
        Self
            a reference to self
        """
        index = self.index(__value)
        self.__delitem__(index)

        self.__rearrange = True
        return self

    def pop(self, __index: SupportsIndex = -1) -> _V:
        """Removes the value at the given index and returns it.

        Parameters
        ----------
        __index : SupportsIndex, optional
            the index to pop, by default -1

        Returns
        -------
        _V
            the value that was at __index

        Note
        ----
        This method does not return a self reference in order to remain consistent with
        the Python list API.
        """
        value = self.__values[__index]
        del self[__index]

        self.__rearrange = True
        return value

    def clear(self) -> Self:
        """Clears all values from the list.

        Returns
        -------
        Self
            a reference to self
        """
        self.__values.clear()
        self.__datas.clear()
        self.__containers.clear()
        self.submobjects.clear()

        return self

    def index(
        self, __value: _V, __start: SupportsIndex, __stop: SupportsIndex = sys.maxsize
    ) -> int:
        """Finds the first instance of __value and returns its index.

        Parameters
        ----------
        __value : _V
            the value to search for
        __start : SupportsIndex
            the index to start searching from
        __stop : SupportsIndex, optional
            the index to stop searching at, by default sys.maxsize

        Returns
        -------
        int
            the index of __value if it is present (ValueError otherwise)
        """
        return self.__values.index(__value, __start, __stop)

    def count(self, __value: _V) -> int:
        """Counts the number of instances of __value.

        Parameters
        ----------
        __value : _V
            the value to count

        Returns
        -------
        int
            the number of times __value occurred
        """
        return self.__values.count(__value)

    def sort(
        self, key: Callable[[_V], SupportsRichComparison] = lambda x: x, reverse=False
    ) -> Self:
        """Sorts the list inplace according to the given key.

        Parameters
        ----------
        key : (_V) -> SupportsRichComparison, optional
            a callable to convert values to a sortable type, by default lambda x: x
        reverse : bool, optional
            False for ascending order, True for descending order, by default False

        Returns
        -------
        Self
            a reference to self
        """
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

    def reverse(self) -> Self:
        """Reverses the order of element

        Returns
        -------
        Self
            _description_
        """
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

        # Update submobjects
        submobject_index = self.__submobject_index(index)
        self.submobjects.__delitem__(submobject_index)
        if self.__delimiter is not None and len(self.submobjects) > 0:
            # Delete last container when delimiting
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

    # Robust copy required for .animate
    def __copy__(self) -> Self:
        """Performs a shallow copy of self.__values and a deepcopy of the graphical components.

        Returns
        -------
        Self
            a copy of this LinearCollection
        """
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

    def copy(self) -> Self:
        """Alias for self.__copy__()

        Returns
        -------
        Self
            a shallow copy of this object
        """
        return self.__copy__()
