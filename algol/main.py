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
            Star(200, x=(lambda s, t, d: 0), y=(lambda s, t, d: 0), z=0),
            Star(
                100,
                x=(lambda s, t, d: math.sin(t) / 2),
                y=(lambda s, t, d: -math.cos(t) / 4),
                z=0,
                color=(1.0, 1.0, 0.0),
            ),
            Star(
                50,
                x=(lambda s, t, d: math.cos(t) / 1.5),
                y=(lambda s, t, d: math.sin(t) / 1.5),
                z=0,
                color=(0.75, 0.50, 0.25),
            ),
        )

        vertex_source = shader_source(
            self._path / "shaders" / "vertex.glsl",
            {"NUMBER_OF_OBJECTS": self._world.size},
        )
        fragment_source = shader_source(self._path / "shaders" / "fragment.glsl")
        self.prog = self.ctx.program(
            vertex_shader=vertex_source, fragment_shader=fragment_source
        )

    def render(self, time, frame_time):
        self.ctx.clear(0.05, 0.05, 0.15)
        self.ctx.enable_only(mgl.PROGRAM_POINT_SIZE | mgl.BLEND)
        self.ctx.blend_func = mgl.ADDITIVE_BLENDING

        self._world.update(time)

        self.prog["radii"] = self._world.radii
        self.prog["colors"] = self._world.colors
        vertices = self._world.vertices
        # print(self._world.colors)
        self.pos_buffer = self.ctx.buffer(np.array(self._world.vertices).astype("f4"))
        self.vao = self.ctx.vertex_array(
            self.prog, [(self.pos_buffer, "3f", "in_position")]
        )
        self.vao.render(mode=mgl.POINTS)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
