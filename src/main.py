import moderngl_window as mglw


class App(mglw.WindowConfig):
    gl_version = (4, 3)
    title = "Algol"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frame_time):
        self.ctx.clear(0.05, 0.05, 0.15)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == "__main__":
    App.run()
