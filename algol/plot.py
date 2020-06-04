import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from itertools import cycle


with open("data.csv", "r") as fp:

    def process_row(row):
        t, l, p = row.split(",")
        return (float(t), float(l), p)

    data = [process_row(line) for line in fp.read().splitlines()[1:]]


presets = {
    "preset1": "#263165",
    "preset2": "#FFAB0B",
    "preset3": "#95eb00",
    "preset4": "#EF5052",
    "preset5": "#45CBF3",
    "preset6": "#6EC388",
    "preset7": "#6D3D1E",
    "preset8": "#FBE929",
    "preset9": "#F5B8D2",
}

patches = []

for p, c in presets.items():
    times = [r[0] for r in data if r[2] == p + ".json"]
    luminances = [r[1] for r in data if r[2] == p + ".json"]
    plt.plot(times, luminances, color=presets[p])
    patches.append(Patch(fc=c, label=p))

plt.legend(handles=patches)
plt.title("Algol plot")
plt.show()
