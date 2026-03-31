import os
import csv
from sys import maxsize as INF
import itertools

# ANSI color codes
COLORS = [31,32,33,34,35,36] # 31: red, 32: green, 33: yellow, 34: blue, 35: magenta, 36: cyan
SEPARATOR = "─"*30

class Logger:
    def __init__(self, *cols, name="log", resume=True,
                 stdout_flag=True, stdout_include=None, stdout_exclude=None, stdout_min_width=10, stdout_track_min=None, stdout_track_max=None, stdout_formatters=None, stdout_init_flag=True, stdout_init_before_log=False, stdout_separator_before_init=False, stdout_separator_after_log=False,
                 csv_flag=True, csv_delimiter=",",
                 wandb_flag=False, wandb_kwargs=None):

        stdout_include = stdout_include if stdout_include else cols
        stdout_exclude = stdout_exclude if stdout_exclude else []
        stdout_track_min = stdout_track_min if stdout_track_min else []
        stdout_track_max = stdout_track_max if stdout_track_max else []
        stdout_cycle_len = min(len(COLORS), len(stdout_track_min)+len(stdout_track_max))
        stdout_formatters = stdout_formatters if stdout_formatters else {}
        
        wandb_kwargs = wandb_kwargs if wandb_kwargs else {}
        wandb_kwargs["id"] = name
        wandb_kwargs["resume"] = "allow" if resume else False
        
        
        self.cols = cols
        self.name = name
        self.resume = resume

        self.stdout_flag = stdout_flag
        self.stdout_include = list(set(stdout_include)-set(stdout_exclude))
        self.stdout_min_width = stdout_min_width
        self.stdout_track_min = stdout_track_min
        self.stdout_cur_min = {name:INF for name in stdout_track_min}
        self.stdout_track_max = stdout_track_max
        self.stdout_cur_max = {name:-INF for name in stdout_track_max}
        self.stdout_color_cycle = itertools.cycle(COLORS[:stdout_cycle_len])
        self.stdout_formatters = stdout_formatters
        self.stdout_init_flag = stdout_init_flag
        self.stdout_init_before_log = stdout_init_before_log
        self.stdout_separator_before_init = stdout_separator_before_init
        self.stdout_separator_after_log = stdout_separator_after_log
        
        self.csv_flag = csv_flag
        self.csv_path = os.path.abspath(name+".csv")
        self.csv_dir = os.path.dirname(self.csv_path)
        self.csv_delimiter = csv_delimiter
        
        self.wandb_flag = wandb_flag
        self.wandb_kwargs = wandb_kwargs
        

        if stdout_flag and stdout_init_flag: self.stdout_init()
        
        if csv_flag: self.csv_init()

        if wandb_flag:
            self.wandb_run = self.wandb_init()
        
    def log(self, *vals):
        if len(self.cols) != len(vals):
            raise ValueError(f"Logger has {len(self.cols)} columns, but {len(vals)} values were passed.")

        if self.stdout_flag:
            if self.stdout_init_before_log: self.stdout_init()
            self.stdout_log(*vals)
        
        if self.csv_flag: self.csv_log(*vals)

        if self.wandb_flag: self.wandb_log(*vals)


    def stdout_init(self):
        if self.stdout_separator_before_init: print(SEPARATOR)
        
        styled_cols = []
        
        for col in self.cols:
            if col not in self.stdout_include:
                continue
            
            if col in self.stdout_formatters:
                prefix = "1;3" # Bold+italics
            else:
                prefix = "1" # Bold
            
            if col in self.stdout_track_min:
                col = col + "(↓)"
                color = next(self.stdout_color_cycle)
                stylize = lambda col: f"\x1b[{prefix};{color}m{col}\x1b[0m"
            elif col in self.stdout_track_max:
                col = col + "(↑)"
                color = next(self.stdout_color_cycle)
                stylize = lambda col: f"\x1b[{prefix};{color}m{col}\x1b[0m"
            else:
                stylize = lambda col: f"\x1b[{prefix}m{col}\x1b[0m"
            width = max(self.stdout_min_width, len(col))
            col = col.rjust(width)
            col = stylize(col)
            styled_cols.append(col)
        
        print(' '.join(styled_cols), flush=True)

    def stdout_log(self, *vals):
        styled_vals = []
        
        for col, val in zip(self.cols, vals):
            if col not in self.stdout_include:
                continue
            
            if col in self.stdout_track_min:
                color = next(self.stdout_color_cycle)
                if val < self.stdout_cur_min[col]:
                    self.stdout_cur_min[col] = val
                    stylize = lambda val: f"\x1b[{color}m{val}\x1b[0m"
                else:
                    stylize = lambda val: val
                styled_col = col + "(↓)"
            elif col in self.stdout_track_max:
                color = next(self.stdout_color_cycle)
                if self.stdout_cur_max[col] < val:
                    self.stdout_cur_max[col] = val
                    stylize = lambda val: f"\x1b[{color}m{val}\x1b[0m"
                else:
                    stylize = lambda val: val
                styled_col = col + "(↑)"
            else:
                stylize = lambda val: val
                styled_col = col
            
            styled_val = self.stdout_formatters[col](val) if col in self.stdout_formatters else val

            if isinstance(styled_val, float):
                styled_val = f"{styled_val:.3f}"
            else:
                styled_val = str(styled_val)
            width = max(self.stdout_min_width, len(styled_col))
            styled_val = styled_val.rjust(width)
            styled_val = stylize(styled_val)
            styled_vals.append(styled_val)
        
        print(' '.join(styled_vals), flush=True)

        if self.stdout_separator_after_log: print(SEPARATOR)
    

    def csv_init(self):
        if not self.resume or (self.resume and not os.path.isfile(self.csv_path)):
            os.makedirs(self.csv_dir, exist_ok=True)
            with open(self.csv_path, "w") as file:
                writer = csv.writer(file, delimiter=self.csv_delimiter)
                writer.writerow(self.cols)

    def csv_log(self, *vals):
        with open(self.csv_path, "a") as file:
            writer = csv.writer(file, delimiter=self.csv_delimiter)
            writer.writerow(vals)
    

    def wandb_init(self):
        import wandb

        run = wandb.init(**self.wandb_kwargs)

        return run
        
    def wandb_log(self, *vals):
        data = dict(zip(self.cols, vals))
        self.wandb_run.log(data)
