# CSVLogger

## Description
CSVLogger is a convenient Python logger. It simultaneously logs data to a CSV file and the terminal (to be expanded in the future). It was made with Machine Learning (ML) in mind.

## Getting Started
1) Install/update(-U) csvlogger from GitHub

```bash
pip install -U git+https://github.com/gvlassis/csvlogger
```

2) Initialize a Logger

```python
import csvlogger

# Two columns of data, logged into example.csv (space-delimited). Only the second one is printed to the terminal, with a minimum width of 20 characters. If the newly printed value is the running minimum, it is colored.
logger = csvlogger.Logger("first_col", "second_col", path="example.csv", delimiter=" ", include=["second_col"], min_width=20, track_min=["second_col"])
```

3) Use the Logger to log data

```python
logger.log(1,2) # Both logged, but only "2" printed (colored)
logger.log(10,20) # Both logged, but only "20" printed
```
