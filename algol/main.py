import os
import math
from pathlib import Path
import json

import moderngl as mgl
import moderngl_window as mglw
from pyrr import Matrix33
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
        self.load_preset("preset1.json")

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
        self.camera_position = (0, 0, 100)
        self.zoom_level = 1
        self.show_checkboard = False

    def load_preset(self, preset):
        joined = os.path.join(os.path.dirname(__file__), "presets", preset)
        if os.path.exists(joined):
            with open(joined, "r") as fp:
                data = json.load(fp)
        else:
            return

        self._world = World()
        self._world.load_dict(data)

        compute_source = shader_source(
            self._path / "shaders" / "compute.glsl",
            {"NUMBER_OF_OBJECTS": self._world.size},
        )
        self.compute = self.ctx.compute_shader(compute_source)

    def render(self, time, frame_time):
        self._world.update(time)

        W, H = self.texture.size

        self.compute["background_color"] = (0.05, 0.05, 0.15)
        self.compute["objects"] = self._world.as_tuples()
        self.compute["colors"] = self._world.colors()
        self.compute["perspective_matrix"].write(self.perspective_matrix)
        self.compute["camera_position"] = self.camera_position
        self.compute["zoom_level"] = self.zoom_level
        self.compute["show_checkboard"] = self.show_checkboard

        self.compute.run(W // 16, H // 16, 1)
        self.texture.use(location=0)
        self.texture.bind_to_image(0, read=False, write=True)
        self.quad_fs.render(self.quad_program)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.Y:
                self.perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype="f4"
                )
                self.camera_position = (0, 0, 100)
            elif key == self.wnd.keys.Z:
                self.perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype="f4"
                )
                self.camera_position = (0, 0, 100)
            elif key == self.wnd.keys.SPACE:
                self.zoom_level = 1
            elif key == self.wnd.keys.TAB:
                self.show_checkboard = not self.show_checkboard
            elif key == self.wnd.keys.NUMBER_1:
                self.load_preset("preset1.json")
            elif key == self.wnd.keys.NUMBER_2:
                self.load_preset("preset2.json")
            elif key == self.wnd.keys.NUMBER_3:
                self.load_preset("preset3.json")
            elif key == self.wnd.keys.NUMBER_4:
                self.load_preset("preset4.json")
            elif key == self.wnd.keys.NUMBER_5:
                self.load_preset("preset5.json")
            elif key == self.wnd.keys.NUMBER_6:
                self.load_preset("preset6.json")
            elif key == self.wnd.keys.NUMBER_7:
                self.load_preset("preset7.json")
            elif key == self.wnd.keys.NUMBER_8:
                self.load_preset("preset8.json")
            elif key == self.wnd.keys.NUMBER_9:
                self.load_preset("preset9.json")

    def mouse_scroll_event(self, x_offset, y_offset):
        multiplier = 1.25 if y_offset > 0 else 0.8
        self.zoom_level = min(max(self.zoom_level * multiplier, 0.25), 10)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
