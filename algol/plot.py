"""Part of Algol program used to plot charts of mean luminance"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from itertools import cycle


with open("data.csv", "r") as fp:

    def process_row(row: str) -> (float, float, str):
        # used to just convert given row of data into usable data
        t, l, p = row.split(",")
        return (float(t), float(l), p[:-5])

    data = [process_row(line) for line in fp.read().splitlines()[1:]]

# presets and colors used to plot their luminance
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

current_times = [data[0][0]]
current_luminances = [data[0][1]]
current_preset = data[0][2]

# patches for legend
patches = []

for row in data[1:]:
    t, l, p = row
    if current_preset != p:
        plt.plot(current_times, current_luminances, color=presets[current_preset])
        patches.append(Patch(fc=presets[current_preset], label=current_preset))
        current_times = []
        current_luminances = []
        current_preset = p
    current_times.append(t)
    current_luminances.append(l)

if current_preset is not None:
    plt.plot(current_times, current_luminances, color=presets[current_preset])
    patches.append(Patch(fc=presets[current_preset], label=current_preset))

    plt.legend(handles=patches)
    plt.title("Algol plot")
    plt.show()
