import sys


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
    situation = {}
    hits = list()
    for line_number, line in enumerate(sys.stdin):
        if line_number == 0:
            continue
        if line_number == 20:
            break
        strokes = line.rstrip().split(" ")
        if line_number < 10:
            for k in range(len(strokes) - 1):
                key = str(strokes[0]) + str(k + 1)
                situation[key] = strokes[k + 1]
        else:
            hits.append(strokes[0])
    sys.stdin.close()
    return situation, hits


output_file_name = "output.txt"
field_situation, opponent_hits = read_data()
output_file = open(output_file_name, 'w', encoding='UTF-8')
for i in range(len(opponent_hits)):
    if field_situation[str(opponent_hits[i])] == 'x':
        sys.stdout.write('Попал!\n')
        output_file.writelines('Попал!\n')
    else:
        sys.stdout.write('Промах!\n')
        output_file.writelines('Промах!\n')
output_file.close()
