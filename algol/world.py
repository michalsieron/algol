import math
from itertools import chain
from abc import ABC, abstractmethod

from pyrr import Vector3, Vector4

from exceptions import AlgolException


class WorldObject(ABC):
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
    def __init__(self):
        self._objects: set = set()

    def load_dict(self, data: dict):
        for star in data.get("stars", []):
            self._objects.add(Star(**star))
        for planet in data.get("planets", []):
            self._objects.add(Planet(**planet))

    @property
    def size(self) -> int:
        return len(self._objects)

    def colors(self) -> [(float, float, float)]:
        return [o.color for o in sorted(self._objects, key=lambda ob: ob.radius)]

    def as_tuples(self) -> [(float, float, float, float)]:
        return [o.as_tuple() for o in sorted(self._objects, key=lambda ob: ob.radius)]

    def update(self, time: float):
        for obj in self._objects:
            obj.update(time)

    def add(self, *objs: [WorldObject]):
        for obj in objs:
            if isinstance(obj, WorldObject):
                self._objects.add(obj)
            else:
                raise AlgolException(repr(obj) + " is not a WorldObject!")
