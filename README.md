# CSVLogger

## Description
CSVLogger is a convenient Python logger. It simultaneously logs data to the terminal, a CSV file and to W&B (to be expanded in the future). It was made with Machine Learning in mind.

## Getting Started
1) Install/update(-U) csvlogger from GitHub

```bash
pip install -U git+https://github.com/gvlassis/csvlogger
```

2) Initialize Logger(s)

```python
import csvlogger

# Super simple logger, with two columns of data. The log is going to be: i) printed to the CLI, ii) saved in `./example.csv`, iii) synced to W&B.
logger1 = csvlogger.Logger("first_column", "second_column", name="example", stdout_flag=True, csv_flag=True, wandb_flag=False)

# ML logger with four columns. The logger resumes from a saved state. All four columns will be logged, but "time" is excluded from printing. The minimum width of every cell in the terminal will be 20 characters. The current minimums of "train_loss" and "val_loss" will be colored. The W&B run id is "gold-magikarp".
logger2 = csvlogger.Logger("epoch", "train_loss", "val_loss", "time", name="ml", resume=True,
                           stdout_flag=True, stdout_exclude=["time"], stdout_min_width=20, stdout_track_min=["train_loss", "val_loss"],
                           csv_flag=True, csv_delimiter=" ",
                           wandb_flag=True, wandb_kwargs={"id":"gold-magikarp"})
```

3) Use the Logger(s) to log data

```python
logger1.log(1,2) # Both logged in ./example.csv, both printed
logger1.log(10,20) # Both logged ./example.csv, both printed

logger2.log(1, 9.8, 9.7, 3) # All logged in ./ml.csv and ./ml_wandb (id=gold-magikarp), but 3 is not printed. 9.8 and 9.7 will be colored.
logger2.log(2, 9.5, 9.9, 4) # All logged in ./ml.csv and ./ml_wandb (id=gold-magikarp), but 4 is not printed. 9.5 will be colored.
```
