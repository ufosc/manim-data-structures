import copy


def exclude_from_deepcopy(*exclude_list):
    """A decorator that overloads the __deepcopy__ method to shallowcopy certain attributes."""

    def deepcopy_with_exclude(self, memo):
        new = type(self).__new__(type(self))
        memo[id(self)] = new
        for k, v in self.__dict__.items():
            if k in exclude_list:
                setattr(new, k, v)
            else:
                setattr(new, k, copy.deepcopy(v, memo))
        return new

    def _(cls):
        setattr(cls, "__deepcopy__", deepcopy_with_exclude)
        return cls

    return _


if __name__ == "__main__":

    @exclude_from_deepcopy("a")
    class Test:
        def __init__(self):
            self.a = [1, 2, 3]

    # Test = exclude_from_deepcopy(Test, "a")

    test_obj = Test()
    test_obj_copy = copy.deepcopy(test_obj)
    test_obj.a.append(4)
    print(test_obj_copy.a)
