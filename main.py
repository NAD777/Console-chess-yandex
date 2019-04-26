from copy import copy

WHITE = 1
BLACK = 2


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


class Rook:

    def __init__(self, color):
        self.color = color
        self.moved = False

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def set_moved(self):
        self.moved = True

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __str__(self):
        return 'R'


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if not (board.field[row1][col1] is None):
            return False
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        if board.g_color(row, col) == board.g_color(row1, col1):
            return False
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))

    def __str__(self):
        return 'P'


class Knight:
    '''Класс коня'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if 0 <= row1 <= 7 and 0 <= col1 <= 7 and (
                (abs(row1 - row) == 1 and abs(col1 - col) == 2) or (
                abs(row1 - row) == 2 and abs(col1 - col) == 1)):
            return True
        else:
            return False

    """
    if 0 <= row <= 7 and 0 <= col <= 7 and (
                (abs(row - self.row) == 1 and abs(col - self.col) == 2) or (
                abs(row - self.row) == 2 and abs(col - self.col) == 1)):
            return True
        else:
            return False
    """

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __str__(self):
        return 'N'


class King:
    '''Класс короля'''

    def __init__(self, color):
        self.color = color
        self.moved = False

    def get_color(self):
        return self.color

    def set_moved(self):
        self.moved = True

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if board.g_color(row1, col1) != self.get_color() \
                and ((abs(row - row1) == 1 and abs(col - col1) == 0) or
                     (abs(row - row1) == 0 and abs(col - col1) == 1) or
                     (abs(row - row1) == 1 and abs(col - col1) == 1)):
            return True
        else:
            return False

    """
    def can_move(self, row, col):
        if self.board.g_color(row, col) != self.g_color() \
                and ((abs(self.row - row) == 1 and abs(self.col - col) == 0) or
                     (abs(self.row - row) == 0 and abs(self.col - col) == 1) or
                     (abs(self.row - row) == 1 and abs(self.col - col) == 1)):
            return True
        else:
            return False
    """

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __str__(self):
        return 'K'


class Queen:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        # print(self.color)
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if correct_coords(row, col) and correct_coords(row1, col1) and \
                board.g_color(row, col) != board.g_color(row1, col1) and \
                (abs(col - col1) == abs(row - row1) or (row == row1 and col != col1) or
                 (row != row1 and col == col1)):
            if row < row1 and col == col1:
                for i in range(row + 1, row1):
                    if not (board.field[i][col] is None):
                        return False
            elif row > row1 and col == col1:
                for i in range(row1 + 1, row):
                    if not (board.field[i][col] is None):
                        return False
            elif row == row1 and col < col1:
                for i in range(col + 1, col1):
                    if not (board.field[row][i] is None):
                        return False
            elif row == row1 and col > col1:
                for i in range(col1 + 1, col):
                    if not (board.field[row][i] is None):
                        return False
            elif row < row1 and col < col1:
                for i in range(1, row1 - row):
                    if not (board.field[row + i][col + i] is None):
                        return False
            elif row > row1 and col > col1:
                for i in range(1, row - row1):
                    if not (board.field[row - i][col - i] is None):
                        return False
            elif row < row1 and col > col1:
                for i in range(1, row1 - row):
                    if not (board.field[row + i][col - i] is None):
                        return False
            elif row > row1 and col < col1:
                for i in range(1, col1 - col):
                    if not (board.field[row - i][col + i] is None):
                        return False
            return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __str__(self):
        return 'Q'


class Bishop:
    '''Класс слона.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if correct_coords(row, col) and correct_coords(row1, col1) and \
                board.g_color(row, col) != board.g_color(row1, col1) and \
                abs(col - col1) == abs(row - row1):
            if row < row1 and col < col1:
                for i in range(1, row1 - row):
                    if not (board.field[row + i][col + i] is None):
                        return False
            elif row > row1 and col > col1:
                for i in range(1, row - row1):
                    if not (board.field[row - i][col - i] is None):
                        return False
            elif row < row1 and col > col1:
                for i in range(1, row1 - row):
                    if not (board.field[row + i][col - i] is None):
                        return False
            elif row > row1 and col < col1:
                for i in range(1, col1 - col):
                    if not (board.field[row - i][col + i] is None):
                        return False
            return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __str__(self):
        return 'B'


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

    def current_player_color(self):
        return self.color

    def castling0(self):
        if self.color == WHITE:
            x_k, y_k = 0, 4
            x1, y1 = 0, 0
        else:
            x_k, y_k = 7, 4
            x1, y1 = 7, 0
        # print(self.get_piece(x_k, y_k).moved)
        if self.get_piece(x_k, y_k).__class__.__name__ == 'King' and \
                not self.get_piece(x_k, y_k).moved:
            if self.field[x1][y1].__class__.__name__ == 'Rook' and \
                    not self.get_piece(x1, y1).moved and \
                    self.get_piece(x1, y1).can_move(self, x1, y1, x_k, y_k) \
                    and self.g_color(x1, y1) == self.g_color(x_k, y_k):
                self.field[x_k][y_k - 1] = self.field[x1][y1]

                self.field[x1][y1] = None
                self.field[x_k][y_k - 2] = self.field[x_k][y_k]
                self.field[x_k][y_k] = None
                self.color = opponent(self.color)
                return True
            else:
                return False
        else:
            return False

    def castling7(self):
        if self.color == WHITE:
            x_k, y_k = 0, 4
            x1, y1 = 0, 7
        else:
            x_k, y_k = 7, 4
            x1, y1 = 7, 7
        # print(self.get_piece(x_k, y_k).moved)
        if self.get_piece(x_k, y_k).__class__.__name__ == 'King' and \
                not self.get_piece(x_k, y_k).moved:
            if self.field[x1][y1].__class__.__name__ == 'Rook' and \
                    not self.get_piece(x1, y1).moved and \
                    self.get_piece(x1, y1).can_move(self, x1, y1, x_k, y_k) \
                    and self.g_color(x1, y1) == self.g_color(x_k, y_k):
                self.field[x_k][y_k + 1] = self.field[x1][y1]

                self.field[x1][y1] = None
                self.field[x_k][y_k + 2] = self.field[x_k][y_k]
                self.field[x_k][y_k] = None
                self.color = opponent(self.color)
                return True
            else:
                return False
        else:
            return False

    # self.color = opponent(self.color)
    # self.field[row][col].__class__.__name__ == 'Pawn'

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if self.field[row][col].__class__.__name__ == 'Pawn' \
                and (self.field[row][col].can_attack(self, row, col, row1, col1) or
                     self.field[row][col].can_move(self, row, col, row1, col1)) \
                and ((self.g_color(row, col) == WHITE and row1 == 7)
                     or (self.g_color(row, col) == BLACK and row1 == 0)) and \
                self.g_color(row, col) != self.g_color(row1, col1):

            if char == 'Q':
                self.field[row1][col1] = Queen(self.g_color(row, col))
            elif char == 'R':
                self.field[row1][col1] = Rook(self.g_color(row, col))
            elif char == 'B':
                self.field[row1][col1] = Bishop(self.g_color(row, col))
            elif char == 'N':
                self.field[row1][col1] = Knight(self.g_color(row, col))
            self.field[row][col] = None
            return True
        else:
            return False

    def g_color(self, row, col):
        if not (self.field[row][col] is None):
            return self.field[row][col].get_color()
        else:
            return -1

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        #
        if piece.get_color() != self.color:
            return False
        # todo uncomment when do last task
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if self.get_piece(row, col).__class__.__name__ == 'King' or \
                self.get_piece(row, col).__class__.__name__ == 'Rook':
            self.get_piece(row, col).set_moved()

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)

        return True

    def pprint(self):
        for line in self.field:
            for el in line:
                print("{:>6}".format(str(el)), end='')
            print()
