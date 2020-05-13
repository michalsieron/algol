import math

from itertools import chain

from pyrr import Vector3, Vector4

from exceptions import AlgolException


class WorldObject:
    @property
    def radius(self) -> float:
        return self._radius

    @property
    def color(self) -> (float, float, float):
        pass

    def update(self, time):
        pass

    def as_tuple(self) -> (float, float, float, float):
        pass


class Star(WorldObject):
    def __init__(self, radius: float, **kwargs):
        self._radius: float = radius
        self._pos: Vector3 = Vector3(kwargs.get("pos", [0.0, 0.0, 0.0]))
        self._x = kwargs.get("x", 0.0)
        self._y = kwargs.get("y", 0.0)
        self._z = kwargs.get("z", 0.0)
        self._color = kwargs.get("color", (1.0, 1.0, 1.0))

    @property
    def radius(self):
        return self._radius

    @property
    def color(self) -> (float, float, float):
        return self._color

    def update(self, time, data: dict = {}):
        if callable(self._x):
            self._pos.x = self._x(self, time, data)
        else:
            self._pos.x = self._x
        if callable(self._y):
            self._pos.y = self._y(self, time, data)
        else:
            self._pos.y = self._y
        if callable(self._z):
            self._pos.z = self._z(self, time, data)
        else:
            self._pos.z = self._z

    def as_tuple(self) -> (float, float, float, float):
        return (*self._pos, self._radius)


class Planet(WorldObject):
    pass


class World:
    def __init__(self):
        self._objects: set = set()

    @property
    def size(self) -> int:
        return len(self._objects)

    def colors(self) -> [(float, float, float)]:
        return [o.color for o in self._objects]

    def as_tuples(self) -> [(float, float, float, float)]:
        return [o.as_tuple() for o in self._objects]

    def update(self, time: float, data: dict = {}):
        for obj in self._objects:
            obj.update(time, data)

    def add(self, *objs: [WorldObject]):
        for obj in objs:
            if isinstance(obj, WorldObject):
                self._objects.add(obj)
            else:
                raise AlgolException(repr(obj) + " is not a WorldObject!")
