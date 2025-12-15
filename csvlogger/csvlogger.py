import os
import csv
from sys import maxsize as INF
import itertools

# ANSI color codes
COLORS = [31,32,33,34,35,36] # 31: red, 32: green, 33: yellow, 34: blue, 35: magenta, 36: cyan

class Logger:
    def __init__(self, *names, path="log.csv", delimiter=",", include=None, exclude=None, min_width=10, track_min=None, track_max=None):
        path = os.path.abspath(path)
        include = include if include else names
        exclude = exclude if exclude else []
        track_min = track_min if track_min else []
        track_max = track_max if track_max else []

        self.names = names
        self.path = path
        self.dir = os.path.dirname(path)
        self.delimiter = delimiter
        self.include = list(set(include)-set(exclude))
        self.min_width = min_width
        self.track_min = track_min
        self.min = {name:INF for name in track_min}
        self.track_max = track_max
        self.max = {name:-INF for name in track_max}
        cycle_len = min(len(COLORS), len(track_min)+len(track_max))
        self.color_cycle = itertools.cycle(COLORS[:cycle_len])
        
        included_names = []
        for name in self.names:
            if name not in self.include:
                continue
            
            if name in self.track_min:
                name = name + "(↓)"
                color = next(self.color_cycle)
                stylize = lambda name: f"\x1b[1;{color}m{name}\x1b[0m"
            elif name in self.track_max:
                name = name + "(↑)"
                color = next(self.color_cycle)
                stylize = lambda name: f"\x1b[1;{color}m{name}\x1b[0m"
            else:
                stylize = lambda name: f"\x1b[1m{name}\x1b[0m"
            width = max(min_width, len(name))
            name = name.rjust(width)
            name = stylize(name)
            included_names.append(name)
        print(' '.join(included_names))
        
        os.makedirs(self.dir, exist_ok=True)
        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(names)
        
    def log(self, *vals):
        included_vals = []
        for name, val in zip(self.names, vals):
            if name not in self.include:
                continue
            
            if name in self.track_min:
                color = next(self.color_cycle)
                if val < self.min[name]:
                    self.min[name] = val
                    stylize = lambda val: f"\x1b[{color}m{val}\x1b[0m"
                else:
                    stylize = lambda val: val
                name = name + "(↓)"
            elif name in self.track_max:
                color = next(self.color_cycle)
                if self.max[name] < val:
                    self.max[name] = val
                    stylize = lambda val: f"\x1b[{color}m{val}\x1b[0m"
                else:
                    stylize = lambda val: val
                name = name + "(↑)"
            else:
                stylize = lambda val: val

            if isinstance(val, float):
                val = f"{val:.3f}"
            else:
                val = str(val)
            width = max(self.min_width, len(name))
            val = val.rjust(width)
            val = stylize(val)
            included_vals.append(val)
        print(' '.join(included_vals))

        with open(self.path, "a") as file:
            writer = csv.writer(file, delimiter=self.delimiter)
            writer.writerow(vals)
