import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


class MapVisualiser:
    map_colors = {
        "O": mcolors.to_rgba("navy"),
        "J": mcolors.to_rgba("forestgreen"),
        "S": mcolors.to_rgba("#e1ab62"),
        "D": mcolors.to_rgba("salmon"),
        "M": mcolors.to_rgba("lightslategrey"),
    }
    map_labels = {
        "O": "Ocean",
        "J": "Jungle",
        "S": "Savannah",
        "D": "Desert",
        "M": "Mountain",
    }

    def __init__(self, map_layout, map_ax, legend_ax):
        self.map_layout = map_layout
        self.map_ax = map_ax
        self.legend_ax = legend_ax

    def generate_map_array(self):
        """Transform the string that parametrises the map into an rgba image.
        """
        lines = self.map_layout.splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells != len(line):
                raise ValueError(
                    "All lines in the map must have the same number of cells."
                )
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError(
                        f"'{letter}' is not a valid landscape type. "
                        f"Must be one of {set(self.map_colors.keys)}"
                    )
                map_array[-1].append(self.map_colors[letter])

        return map_array

    def visualise(self):
        """Create a map over the island
        """
        self.map_ax.imshow(self.generate_map_array())
        for i, (landscape, color) in enumerate(self.map_colors.items()):
            label = self.map_labels[landscape]
            self.legend_ax.add_patch(
                plt.Rectangle(
                    (0.0, i * 0.2),
                    width=0.1,
                    height=0.1,
                    edgecolor=None,
                    facecolor=color,
                )
            )
            self.legend_ax.text(
                x=0.2,
                y=0.05 + i * 0.2,
                s=self.map_labels[landscape],
                verticalalignment="center",
                weight="bold",
                size=18,
            )

        self.legend_ax.axis("off")
        self.legend_ax.set_ylim(0, i * 0.2 + 0.1)


if __name__ == "__main__":
    map_layout = """\
OOOO
OJSO
OMDO
OOOO
"""
    fig, (map_ax, legend_ax) = plt.subplots(1, 2)
    vis = MapVisualiser(map_layout, map_ax, legend_ax)
    vis.visualise()
    plt.show()
