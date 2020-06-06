import math
from itertools import chain
from abc import ABC, abstractmethod

from pyrr import Vector3, Vector4

from exceptions import AlgolException


class WorldObject(ABC):
    """
    Base class for objects simulated in Algol.
    Use this as parent class to create new types of objects.
    """

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def pos(self) -> Vector3:
        return self._pos

    @property
    def center(self) -> Vector3:
        return self._center

    @property
    def axes_lengths(self) -> Vector3:
        return self._axes_lengths

    @property
    def velocities(self) -> Vector3:
        return self._velocities

    @property
    def phase(self) -> Vector3:
        return self._phase

    @property
    def color(self) -> (float, float, float):
        return self._color

    @abstractmethod
    def update(self, time):
        pass

    @abstractmethod
    def as_tuple(self) -> (float, float, float, float):
        pass


class Star(WorldObject):
    """Represents star objects in Algol"""

    def __init__(self, radius: float, **kwargs):
        self._radius: float = radius
        self._pos: Vector3 = Vector3([0.0, 0.0, 0.0])
        self._center: Vector3 = Vector3(kwargs.get("center", [0.0, 0.0, 0.0]))
        self._axes_lengths: Vector3 = Vector3(
            kwargs.get("axes_lengths", [0.0, 0.0, 0.0])
        )
        self._velocities: Vector3 = Vector3(kwargs.get("velocities", [0.0, 0.0, 0.0]))
        self._phase: Vector3 = Vector3(kwargs.get("phase", [0.0, 0.0, 0.0]))
        self._color: (float, float, float) = tuple(kwargs.get("color", (1.0, 1.0, 1.0)))

    def update(self, time):
        temp = self._velocities * time + self._phase
        self._pos = (self._axes_lengths / 2.0) * Vector3(
            [math.sin(temp.x), math.sin(temp.y), math.cos(temp.z)]
        ) + self._center

    def as_tuple(self) -> (float, float, float, float):
        return (*self._pos, self._radius)


class Planet(WorldObject):
    """Represents planet objects in Algol"""

    def __init__(self, radius: float, **kwargs):
        self._radius: float = radius
        self._pos: Vector3 = Vector3([0.0, 0.0, 0.0])
        self._center: Vector3 = Vector3(kwargs.get("center", [0.0, 0.0, 0.0]))
        self._axes_lengths: Vector3 = Vector3(
            kwargs.get("axes_lengths", [0.0, 0.0, 0.0])
        )
        self._velocities: Vector3 = Vector3(kwargs.get("velocities", [0.0, 0.0, 0.0]))
        self._phase: Vector3 = Vector3(kwargs.get("phase", [0.0, 0.0, 0.0]))
        self._color: (float, float, float) = (0.0, 0.0, 0.0)

    def update(self, time):
        temp = self._velocities * time + self._phase
        self._pos = (self._axes_lengths / 2.0) * Vector3(
            [math.sin(temp.x), math.sin(temp.y), math.cos(temp.z)]
        ) + self._center

    def as_tuple(self) -> (float, float, float, float):
        return (*self._pos, self._radius)


class World:
    """Stores `WorldObject`s and provides methods to represent them"""

    def __init__(self):
        self._objects: set = set()

    def load_dict(self, data: dict):
        """Loads `World` state from a `dict`"""
        for star in data.get("stars", []):
            self._objects.add(Star(**star))
        for planet in data.get("planets", []):
            self._objects.add(Planet(**planet))

    @property
    def size(self) -> int:
        """Returns number of objects in a `World`"""
        return len(self._objects)

    def colors(self) -> [(float, float, float)]:
        """Returns colors of `WorldObject`s"""
        return [o.color for o in sorted(self._objects, key=lambda ob: ob.radius)]

    def as_tuples(self) -> [(float, float, float, float)]:
        """Returns a `list` of `tuple`s of 4 `float`s representing `WorldObject`s position and radius"""
        return [o.as_tuple() for o in sorted(self._objects, key=lambda ob: ob.radius)]

    def update(self, time: float):
        """Updates all stored `WorldObject`s by given time"""
        for obj in self._objects:
            obj.update(time)

    def add(self, *objs: [WorldObject]):
        """Adds given object(s) to a `World`"""
        for obj in objs:
            if isinstance(obj, WorldObject):
                self._objects.add(obj)
            else:
                raise AlgolException(repr(obj) + " is not a WorldObject!")
