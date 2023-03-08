import copy
from typing import Iterable, List

import numpy as np
from manim import RIGHT, Integer, Mobject, Square, VMobject


class LinearCollection(VMobject):
    __data: List[Mobject]
    __data_template: Mobject
    __container_template: Mobject
    __delimiter: Mobject
    __direction: np.ndarray

    def __init__(
        self,
        data: Iterable,
        data_template=Integer,
        container_template=Square,
        delimiter=None,
        direction=RIGHT,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__data = []
        self.__data_template = data_template
        self.__container_template = container_template
        self.__delimiter = delimiter
        self.__direction = direction

        for value in data:
            self.__data.append(data_template(value))
            new_container = container_template()
            new_container.add(self.__data[-1])
            self.add(new_container)

        self.arrange(direction=self.__direction)

    def insert(self, value):
        self.__data.append(self.__data_template(value))
        new_container = self.__container_template()
        new_container.add(self.__data[-1])
        self.add(new_container)
        self.arrange(direction=self.__direction)

    def remove(self):
        pass

    def __getitem__(self, key):
        return self.__data.__getitem__(key).get_value()

    def __setitem__(self, key, value):
        return self.__data.__getitem__(key).set_value(value)

    def __iter__(self):
        # Initialize a Data iterator when we start iterating
        self.__iter__data = iter(self.__data)
        return self

    def __next__(self):
        try:
            # Return the value of the next Data in the iterator
            return next(self.__iter__data).get_value()
        except StopIteration as e:
            # Clean up the iterator when we're done
            del self.__iter__data
            raise e

    def __add__(self, rhs):
        self_copy = copy.copy(self)
        for container in rhs.submobjects:
            self_copy.add(copy.copy(container))
        for data in rhs._LinearCollection__data:
            self_copy.__data.append(copy.copy(data))

        return self_copy
