import json
import os


def shader_source(path: str, data: dict = {}) -> str:
    with open(path, "r") as fp:
        rtn: str = fp.read()

    for old, new in data.items():
        rtn = rtn.replace(f"%%{old}%%", str(new))

    return rtn


def load_preset(filename: str):
    joined = os.path.join(os.path.dirname(__file__), "presets", filename)
    print(joined)
    if os.path.exists(joined):
        with open(joined, "r") as fp:
            data = json.load(fp)
    else:
        data = {}

    return data
