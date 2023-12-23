class LockedDictClass:

    def __setattr__(self, name, value):
        if "locked" in self.__dict__.keys():
            raise NameError("Class is locked can not add any attributes (%s)" % name)
        if name in self.__dict__.keys():
            raise NameError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value


class LockedSlotClass:

    __slots__: tuple[str] = tuple()

    def __setattr__(self, name, value):
        if "locked" in self.__slots__:
            raise NameError("class is locked")
        if name in self.__slots__:
            raise NameError("class attributes cannot change values")
        if name not in self.__slots__:
            raise NameError("you cannot add attributes to this object")


class Child:

    __slots__ = "alpha", "beta", "locked"

    def __init__(self):
        setattr(self, "alpha", 4)
        self.beta: int = 6
        self.locked: bool = True
        return


if __name__ == "__main__":
    # { slot: getattr(self, slot) for slot in self.__slots__ }
    child = Child()
    print(child.__slots__)
    # child.gamma = 4
