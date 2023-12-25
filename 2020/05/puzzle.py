import fileinput
import numpy as np

x = [line.strip() for line in fileinput.input()]

all_seats = np.zeros(shape=(128, 8))

id_max = -1
for entry in x:
    binary_row = entry[0:7].replace("F", "0").replace("B", "1")
    row = int(binary_row, 2)
    binary_column = entry[-3:].replace("L", "0").replace("R", "1")
    column = int(binary_column, 2)
    id = row*8 + column
    all_seats[row, column] = 1
    if id > id_max:
        id_max = id
print("max id", id_max)

for i, row in enumerate(all_seats):
    if sum(row==1) == 7:
        column = next(i for i in range(8) if row[i] == 0)
        id = i*8 + column
        print("id", id)
