import csv
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import math

def extract_col(csv_file, column_index):
    column_array = []

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) > column_index:
                column_value = row[column_index]
                if column_value != '':
                    column_array.append(column_value)

    return column_array

def user_prompt():
    var1 = input("Enter first statistic: ")
    var2 = input("Enter second statistic: ")
    return var1, var2

def nice_ticks(min_val, max_val, num_ticks):
    range_val = max_val - min_val
    interval = range_val / (num_ticks - 1)
    nice_interval = 10 ** math.floor(math.log10(interval))

    nice_range = nice_interval * math.ceil(range_val / nice_interval)
    nice_min = math.floor(min_val / nice_interval) * nice_interval
    nice_max = nice_min + nice_range

    ticks = np.linspace(nice_min, nice_max, num_ticks)
    return ticks.astype(int)
