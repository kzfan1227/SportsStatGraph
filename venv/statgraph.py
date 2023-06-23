import csv
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import math
from methods import *


#file_name = input("Choose season (20XX-XX): ") + "nba.csv"
#print(file_name)
file_name = "2022-23nba.csv"
with open(file_name, "r") as csv_file:
    reader = csv.reader(csv_file)
    first_row = next(reader)

names = extract_col(file_name, 1)
n1 = names.pop(0)


# User has multiple chances to type right statistics
var1 = ""
var2 = ""
is_invalid = True
while is_invalid:
    var1, var2 = user_prompt()
    try:
        index = first_row.index(var1)
        index2 = first_row.index(var2)
        #check1 = int(extract_col(file_name, first_row.index(var1))[2])
        #check2 = int(extract_col(file_name, first_row.index(var2))[2])
        is_invalid = False
    except ValueError:
        print("Please try again.")

p1 = extract_col(file_name, first_row.index(var1))
p2 = extract_col(file_name, first_row.index(var2))
rem1 = p1.pop(0)
rem2 = p2.pop(0)

gpinrange = False
while gpinrange is False:
    minGP_input = input("Minimum games played? (0 to 83): ")
    try:
        min_gp = int(minGP_input)
        if 0 <= min_gp <= 83:
            gpinrange = True
        else:
            print("Please enter a number from 0-83.")
    except ValueError:
        print("Please enter a valid integer.")


# Removes players that have not played enough games
count = 0
indexes_to_remove = []
gamesplayedarr = extract_col(file_name, 5)
throwaway = gamesplayedarr.pop(0)
for i, m in enumerate(gamesplayedarr):
    if int(m) <= min_gp:
        indexes_to_remove.append(i)
    count += 1

for index in sorted(indexes_to_remove, reverse=True):
    del p1[index]
    del p2[index]
    del names[index]

# Update the remaining elements count
count = len(p1)

# Convert column values to float
arr1 = np.array(p1).astype(float)
arr2 = np.array(p2).astype(float)

fig, ax = plt.subplots()
scatter = ax.scatter(arr1, arr2)

# Set a fixed number of x-axis ticks
num_ticks = 11

# Calculate x-axis tick values based on the range of arr1
min_val = np.min(arr1)
max_val = np.max(arr1)

# For decimal-heavy stats
if max_val < 1.5:
    x_ticks = np.arange(int(min_val*10), int(max_val*10) + 5, 1) / 10  # Scale values by 0.1
else:
    x_ticks = nice_ticks(min_val, max_val, 6)
plt.xticks(x_ticks)

# Calculate y-axis tick values based on the range of arr2
min_val = np.min(arr2)
max_val = np.max(arr2)

if max_val < 1.5:
    y_ticks = np.arange(int(min_val*10), int(max_val*10) + 5, 1) / 10  # Scale values by 0.1
else:
    y_ticks = nice_ticks(min_val, max_val, 6)
plt.yticks(y_ticks)

plt.xlabel(rem1)
plt.ylabel(rem2)

def on_hover(event):
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            index = ind["ind"][0]
            for i, label in enumerate(labels):
                if i == index:
                    label.set_visible(True)
                    label.set_text(f"{names[i]}, {arr1[i]:.2f}, {arr2[i]:.2f}")
                else:
                    label.set_visible(False)
            fig.canvas.draw()
labels = []
for i in range(count):
    label = ax.annotate(names[i],
        (arr1[i], arr2[i]),
        textcoords="offset points",
        xytext=(0, 10),
        ha='center',
        visible=False
    )
    labels.append(label)

fig.canvas.mpl_connect("motion_notify_event", on_hover)

plt.show()