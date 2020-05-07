def shader_source(path: str, data: dict = {}) -> str:
    with open(path, "r") as fp:
        rtn: str = fp.read()

    for old, new in data.items():
        rtn = rtn.replace(f"%%{old}%%", str(new))

    return rtn
