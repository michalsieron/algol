import os
import math
from pathlib import Path

import moderngl as mgl
import moderngl_window as mglw
import numpy as np

from utils import shader_source
from world import World, Star


class App(mglw.WindowConfig):
    gl_version = (4, 3)
    title = "Algol"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._path = Path(os.path.dirname(__file__))

        W, H = App.window_size
        self._world = World()
        self._world.add(
            Star(200, x=(W / 2), y=(H / 2), z=0),
            Star(
                100,
                x=(lambda s, t, d: W / 3 * math.sin(t) + W / 2),
                y=(H / 2),
                z=(lambda s, t, d: 100 * math.cos(t)),
                color=(1.0, 1.0, 0.0),
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

    def render(self, time, frame_time):
        self._world.update(time)

        w, h = self.texture.size
        gw, gh = 16, 16
        nx, ny, nz = w // gw, h // gh, 1

        self.compute["background_color"] = (0.05, 0.05, 0.15)
        self.compute["objects"] = self._world.as_tuples()
        self.compute["colors"] = self._world.colors()

        self.texture.bind_to_image(0, read=False, write=True)
        self.compute.run(nx, ny, nz)
        self.texture.use(location=0)
        self.quad_fs.render(self.quad_program)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
