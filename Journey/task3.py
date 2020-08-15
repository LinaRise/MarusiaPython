import sys

import numpy as np


class GameField:
    size = None

    situation = None

    def __init__(self, size, situation=None):
        self.size = size
        self.situation = situation

    def check_winner(self, symbol):
        return self.check_horizontal_and_vertical(symbol) or self.check_diagonals(symbol)

    def check_diagonals(self, symbol):
        toright = toleft = True
        for i in range(self.size):
            toright &= (self.situation[i][i] == symbol)
            toleft &= (self.situation[self.size - i - 1][i] == symbol)

        return toright or toleft

    def check_horizontal_and_vertical(self, symbol):
        for col in range(self.size):
            columns = True
            rows = True

            for row in range(self.size):
                columns &= (self.situation[col][row] == symbol)
                rows &= (self.situation[row][col] == symbol)
            if columns or rows:
                return True

        return False


def read_data():
    situation = [[]]
    for line_number, line in enumerate(sys.stdin):
        situation.insert(line_number, list((line.rstrip().split(" "))))
        print(situation[line_number])
    situation_array = np.array([np.array(xi) for xi in situation])
    return len(situation[0]), situation_array


def find_indexes(sit, value):
    j = None
    i = None
    for i in range(len(sit[0])):
        for j in range(len(sit[0])):
            if sit[i][j] == value:
                return i, j
    return None


output_file_name = "output.txt"
field_size, situation_on_field = read_data()
print(field_size)
cells_been_to = np.array([[False] * field_size] * field_size)

ix, jy = find_indexes(situation_on_field, 'x')

cells_been_to[ix][jy] = True

print(ix, ';', jy)

output_file = open(output_file_name, 'w', encoding='utf-8')
while True:
    if jy + 1 >= field_size or jy - 1 < 0 or ix + 1 >= field_size or ix - 1 < 0:
        break

    if situation_on_field[ix + 1][jy] == '.':
        if not cells_been_to[ix + 1][jy]:
            ix = ix + 1
            cells_been_to[ix][jy] = True
            sys.stdout.write('Вниз!\n')
            output_file.writelines('Вниз!\n')
    if situation_on_field[ix - 1][jy] == '.':
        if not cells_been_to[ix - 1][jy]:
            ix = ix - 1
            cells_been_to[ix][jy] = True
            sys.stdout.write('Вверх!\n')
            output_file.writelines('Вверх!\n')
    if situation_on_field[ix][jy + 1] == '.':
        # print("!!!!!!")
        if not cells_been_to[ix][jy + 1]:
            jy = jy + 1
            cells_been_to[ix][jy] = True
            sys.stdout.write('Направо!\n')
            output_file.writelines('Направо!\n')
    if situation_on_field[ix][jy - 1] == '.':
        if not cells_been_to[ix][jy - 1]:
            jy = jy - 1
            cells_been_to[ix][jy] = True
            sys.stdout.write('Налево!\n')
            output_file.writelines('Налево!\n')
sys.stdout.flush()
output_file.close()
