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

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

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
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    '''Класс короля'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if board.get_color(row1, col1) != self.get_color() \
                and ((abs(row - row1) == 1 and abs(col - col1) == 0) or
                     (abs(row - row1) == 0 and abs(col - col1) == 1) or
                     (abs(row - row1) == 1 and abs(col - col1) == 1)):
            return True
        else:
            return False

    """
    def can_move(self, row, col):
        if self.board.get_color(row, col) != self.get_color() \
                and ((abs(self.row - row) == 1 and abs(self.col - col) == 0) or
                     (abs(self.row - row) == 0 and abs(self.col - col) == 1) or
                     (abs(self.row - row) == 1 and abs(self.col - col) == 1)):
            return True
        else:
            return False
    """

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if correct_coords(row, col) and correct_coords(row1, col1) and \
                board.get_color(row, col) != board.get_color(row1, col1) and \
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
                board.get_color(row, col) != board.get_color(row1, col1) and \
                ((row == row1 and col != col1) or (row != row1 and col == col1)):
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
            return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

    def current_player_color(self):
        return self.color

    def get_color(self, row, col):
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
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def pprint(self):
        for line in self.field:
            for el in line:
                print("{:>6}".format(str(el)), end='')
            print()
