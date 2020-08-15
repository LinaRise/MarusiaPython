import sys


class GameField:
    size = None

    situation = None

    def __init__(self, size, situation):
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
    size = -2
    situation = [[]]
    for line_number, line in enumerate(sys.stdin):
        if line_number - 1 == size:
            break
        if line_number == 0:
            size = int(line.rstrip())
            continue
        else:
            situation.insert(line_number - 1, list((line.rstrip().split(" "))))
    sys.stdin.close()
    return size, situation


output_file_name = "output.txt"
field_size, situation_on_field = read_data()
game_field = GameField(field_size, situation_on_field)
output_file = open(output_file_name, 'w', encoding='utf-8')
if game_field.check_winner('x'):
    sys.stdout.write('x')
    output_file.writelines('x')
    output_file.close()
elif game_field.check_winner('0'):
    sys.stdout.write('0')
    output_file.writelines('0')
    output_file.close()
else:
    sys.stdout.write('x0')
    output_file.writelines('x0')
    output_file.close()
