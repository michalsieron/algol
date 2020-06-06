import os
import math
import json

import moderngl_window as mglw
from pyrr import Matrix33
import numpy as np

from world import World
from logger import Logger
from exceptions import AlgolException


class App(mglw.WindowConfig):
    """Base class used to run Algol"""

    # OpenGL 4.3 needed for compute shaders
    gl_version = (4, 3)
    title = "Algol"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._path = os.path.dirname(__file__)

        # logger instance for logging events
        self._logger = Logger(os.path.dirname(self._path), "algol.log")
        self._logger.log("Program started")
        self._active_preset = None
        self.load_preset("preset1.json")

        # used to store texture data when calculating luminance
        self._temp_texture_buffer = np.empty(1280 * 720 * 4, dtype="uint8")
        # used to log data measured
        self._data_file = open("data.csv", "w")

        # shaders preparation
        vertex_source = self.shader_source("vertex.glsl")
        fragment_source = self.shader_source("fragment.glsl")
        self._quad_program = self.ctx.program(
            vertex_shader=vertex_source, fragment_shader=fragment_source
        )
        self._quad_fs = mglw.geometry.quad_fs()
        self._texture = self.ctx.texture((1280, 720), 4)

        compute_source = self.shader_source(
            "compute.glsl", {"NUMBER_OF_OBJECTS": self._world.size}
        )
        self._compute = self.ctx.compute_shader(compute_source)

        # variables remembering some user settings for runtime
        self._perspective_matrix = Matrix33(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype="f4"
        )
        self._camera_position = (0, 0, 100)
        self._zoom_level = 1
        self._show_checkerboard = False

    @property
    def camera_position(self) -> (float, float, float):
        """Returns camera position"""
        return self._camera_position

    @property
    def zoom_level(self) -> float:
        """Returns zoom level"""
        return self._zoom_level

    @property
    def show_checkerboard(self) -> bool:
        """Returns `bool` value whether checkerboard should be shown"""
        return self._show_checkerboard

    def shader_source(self, shader, data: dict = {}) -> str:
        """
        Opens shader file and replaces strings in define section.
        Defines are between double percentage characters, but you only
        need to provide `dict` with strings between them as keys
        """
        joined = os.path.join(self._path, "shaders", shader)
        if not os.path.exists(joined):
            raise AlgolException(f"Missing shader file: {shader}")

        with open(joined, "r") as fp:
            rtn: str = fp.read()

        for old, new in data.items():
            rtn = rtn.replace(f"%%{old}%%", str(new))

        self._logger.log(f"Shader file '{shader}' read")
        return rtn

    def load_preset(self, preset):
        """Reads preset files stored as json and creates new `World`"""
        joined = os.path.join(self._path, "presets", preset)
        self._logger.log(f"'{preset}' preset selected")
        if not os.path.exists(joined):
            self._logger.log(f"'{preset}' preset not found")
            return

        with open(joined, "r") as fp:
            data = json.load(fp)
        self._world = World()
        self._world.load_dict(data)
        self._active_preset = preset

        compute_source = self.shader_source(
            "compute.glsl", {"NUMBER_OF_OBJECTS": self._world.size}
        )
        self._compute = self.ctx.compute_shader(compute_source)

    def render(self, time, frame_time):
        self._world.update(time)

        W, H = self._texture.size

        # feeding data to compute shader
        self._compute["background_color"] = (0.05, 0.05, 0.15)
        self._compute["objects"] = self._world.as_tuples()
        self._compute["colors"] = self._world.colors()
        self._compute["perspective_matrix"].write(self._perspective_matrix)
        self._compute["camera_position"] = self.camera_position
        self._compute["zoom_level"] = self.zoom_level
        self._compute["show_checkerboard"] = self.show_checkerboard

        self._compute.run(W // 16, H // 16, 1)
        self._texture.use(location=0)
        self._texture.bind_to_image(0, read=False, write=True)
        self._quad_fs.render(self._quad_program)

        # calculating mean luminance
        self._texture.read_into(self._temp_texture_buffer)
        mean_luminance = np.mean(self._temp_texture_buffer[::4])
        self._data_file.write(f"{time},{mean_luminance},{self._active_preset}\n")

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_RELEASE:
            # perspective
            if key == self.wnd.keys.Y:
                self._perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype="f4"
                )
                self._camera_position = (0, 0, 100)
                self._logger.log("Perspective changed to side view")
            elif key == self.wnd.keys.Z:
                self._perspective_matrix = Matrix33(
                    [[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype="f4"
                )
                self._camera_position = (0, 0, 100)
                self._logger.log("Perspective changed to top view")
            # zoom reset
            elif key == self.wnd.keys.SPACE:
                self._zoom_level = 1
                self._logger.log("Zoom level reset")
            # checkerboard
            elif key == self.wnd.keys.TAB:
                self._show_checkerboard = not self.show_checkerboard
                self._logger.log(
                    "Checkerboard has been " + "shown"
                    if self.show_checkerboard
                    else "hidden"
                )
            # presets
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
        self._zoom_level = min(max(self.zoom_level * multiplier, 0.25), 10)
        self._logger.log(f"Zoom level changed to {self.zoom_level}")

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
