import os
import math
from pathlib import Path
from random import uniform

import moderngl as mgl
import moderngl_window as mglw
import pyglet
import numpy as np
from pyrr import Matrix33

from utils import shader_source
from world import World, Star

instance = None


class App(mglw.WindowConfig):
    gl_version = (4, 3)
    title = "Algol"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global instance
        instance = self

        self._path = Path(os.path.dirname(__file__))

        W, H = App.window_size
        self._world = World()
        self._world.add(
            Star(
                2,
                x=(lambda s, t, d: 0),
                y=(lambda s, t, d: 0),
                z=(lambda s, t, d: 0),
                color=(1.0, 1.0, 1.0),
            ),
            Star(
                1,
                x=(lambda s, t, d: 8 * math.sin(t)),
                y=(lambda s, t, d: 0),
                z=(lambda s, t, d: 10 * math.cos(t)),
                color=(1.0, 1.0, 0.0),
            ),
            Star(
                0.5,
                x=(lambda s, t, d: 16 * math.sin(t * 0.9)),
                y=(lambda s, t, d: math.cos(t)),
                z=(lambda s, t, d: 16 * math.cos(t * 0.9)),
                color=(0.0, 1.0, 1.0),
            ),
            Star(
                0.2,
                x=(lambda s, t, d: 4 * math.sin(t * 1.5)),
                y=0,
                z=(lambda s, t, d: 4 * math.cos(t * 1.5)),
                color=(1.0, 0.0, 1.0),
            ),
        )

        vertex_source = shader_source(self._path / "shaders" / "vertex.glsl")
        fragment_source = shader_source(self._path / "shaders" / "fragment.glsl")
        self.quad_program = self.ctx.program(
            vertex_shader=vertex_source, fragment_shader=fragment_source
        )
        self.quad_fs = mglw.geometry.quad_fs()
        self.texture = self.ctx.texture((1280, 720), 4)

        compute_source = shader_source(
            self._path / "shaders" / "compute.glsl",
            {"NUMBER_OF_OBJECTS": self._world.size},
        )
        self.compute = self.ctx.compute_shader(compute_source)
        self.perspective_matrix = Matrix33(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype="f4"
        )
        self.camera_position = (0, 0, 20)
        self.zoom_level = 1

    def render(self, time, frame_time):
        self._world.update(time)

        W, H = self.texture.size

        self.compute["background_color"] = (0.05, 0.05, 0.15)
        self.compute["objects"] = self._world.as_tuples()
        self.compute["colors"] = self._world.colors()
        self.compute["perspective_matrix"].write(self.perspective_matrix)
        self.compute["camera_position"] = self.camera_position
        self.compute["zoom_level"] = self.zoom_level

        self.compute.run(W, H, 1)
        self.texture.use(location=0)
        self.texture.bind_to_image(0, read=False, write=True)
        self.quad_fs.render(self.quad_program)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.Y:
                self.perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype="f4"
                )
                self.camera_position = (0, 0, 20)
            elif key == self.wnd.keys.Z:
                self.perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype="f4"
                )
                self.camera_position = (0, 0, 20)
            elif key == self.wnd.keys.SPACE:
                self.zoom_level = 1

    def mouse_scroll_event(self, x_offset, y_offset):
        self.zoom_level = min(max(self.zoom_level + y_offset / 10, 0), 10)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
