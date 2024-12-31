import pygame
from Const import *


class Checker:
    def __init__(self, color, row, col, white_img, black_img):
        """Инициализация отдельной шашки."""
        self.color = color
        self.row = row
        self.col = col
        self.white_img = white_img
        self.black_img = black_img

    def draw(self, screen):
        """Отображает шашку на экране."""
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE
        img = self.white_img if self.color == "W" else self.black_img
        screen.blit(img, (x, y))

    def move(self, new_row, new_col):
        """Перемещает шашку в новую клетку."""
        self.row = new_row
        self.col = new_col


class ClassChecker:
    def __init__(self, screen):
        self.screen = screen
        self.current_color = MOVE_WHITE  # Изначально ходит белый игрок
        self.result_game = None
        # Загрузка изображений шашек
        self.white_checker_img = pygame.image.load("image/white-regular.png")
        self.black_checker_img = pygame.image.load("image/black-regular.png")
        # Масштабируем изображения под размер клетки
        self.white_checker_img = pygame.transform.scale(self.white_checker_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_checker_img = pygame.transform.scale(self.black_checker_img, (SQUARE_SIZE, SQUARE_SIZE))
        # Инициализация шашек
        self.checkers = []
        self.selected_checker = None
        self.initialize_checkers()

    def initialize_checkers(self):
        """Создает начальную расстановку шашек."""
        self.current_color = MOVE_WHITE  # Изначально ходит белый игрок
        self.result_game = None
        self.checkers = []
        self.selected_checker = None
        for row in range(ROWS):
            for col in range(COLS):
                if row in [ROWS - 3, ROWS - 1]:
                    # Добавляем белую шашку
                    self.checkers.append(Checker("W", row, col, self.white_checker_img, self.black_checker_img))
                elif row in [0, 2]:
                    # Добавляем черную шашку
                    self.checkers.append(Checker("B", row, col, self.white_checker_img, self.black_checker_img))

    def draw_checkers(self):
        """Рисует все шашки на доске."""
        for checker in self.checkers:
            checker.draw(self.screen)
        if self.selected_checker:
            self.draw_selected_square()
            self.draw_valid_moves()

    def draw_selected_square(self):
        """Подсвечивает выбранную клетку."""
        x = self.selected_checker.col * SQUARE_SIZE
        y = self.selected_checker.row * SQUARE_SIZE
        pygame.draw.rect(self.screen, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_valid_moves(self):
        """Отображает все валидные ходы для выбранной шашки."""
        valid_moves = self.get_valid_moves(self.selected_checker)
        for move in valid_moves:
            x = move[1] * SQUARE_SIZE
            y = move[0] * SQUARE_SIZE
            pygame.draw.rect(self.screen, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def get_valid_moves(self, checker):
        """Возвращает список всех валидных ходов для данной шашки."""
        valid_moves = []
        if not checker:
            return valid_moves

        # Проверяем ходы по горизонтали и вертикали
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            row, col = checker.row, checker.col
            while 0 <= row + dr < ROWS and 0 <= col + dc < COLS:
                row += dr
                col += dc
                if self.get_checker_at(row, col) is not None:
                    break  # Нельзя перескакивать через другие шашки
                valid_moves.append((row, col))
        return valid_moves

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, position):
        """Обработка кликов мыши для выбора и перемещения шашек."""
        col = position[0] // SQUARE_SIZE
        row = position[1] // SQUARE_SIZE
        clicked_checker = self.get_checker_at(row, col)
        if 0 <= col < COLS and 0 <= row < ROWS:
            if clicked_checker and clicked_checker.color == self.current_color:
                # Выбор шашки текущего игрока
                self.selected_checker = clicked_checker
            elif self.selected_checker and (row, col) in self.get_valid_moves(self.selected_checker):
                # Ход для выбранной шашки
                self.selected_checker.move(row, col)
                self.check_and_remove_captured(self.selected_checker)  # Проверяем съедание
                self.selected_checker = None
                self.switch_turn()

    def check_and_remove_captured(self, checker):
        """Проверяет и удаляет шашки, захваченные после хода."""
        captured_checkers = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Проверка всех направлений
        for dr, dc in directions:
            # Проверяем захват между двумя шашками противника
            opposite_row = checker.row - dr
            opposite_col = checker.col - dc
            adjacent_row = checker.row + dr
            adjacent_col = checker.col + dc

            if (
                    self.is_in_bounds(adjacent_row, adjacent_col) and
                    self.is_in_bounds(opposite_row, opposite_col)
            ):
                adjacent_checker = self.get_checker_at(adjacent_row, adjacent_col)
                opposite_checker = self.get_checker_at(opposite_row, opposite_col)

                if (
                        adjacent_checker and adjacent_checker.color != checker.color and
                        opposite_checker and opposite_checker.color != checker.color
                ):
                    captured_checkers.append(adjacent_checker)
                    captured_checkers.append(opposite_checker)
                    continue

            # Проверяем захват шашки между текущей шашкой и другой шашкой того же цвета
            opposite_row = checker.row + dr * 2
            opposite_col = checker.col + dc * 2
            if (
                    self.is_in_bounds(adjacent_row, adjacent_col) and
                    self.is_in_bounds(opposite_row, opposite_col)
            ):
                adjacent_checker = self.get_checker_at(adjacent_row, adjacent_col)
                opposite_checker = self.get_checker_at(opposite_row, opposite_col)

                if (
                        adjacent_checker and adjacent_checker.color != checker.color and
                        opposite_checker and opposite_checker.color == checker.color
                ):
                    captured_checkers.append(adjacent_checker)

        # Удаляем захваченные шашки
        for captured_checker in set(captured_checkers):
            self.checkers.remove(captured_checker)

    @staticmethod
    def is_in_bounds(row, col):
        """Проверяет, находится ли клетка в пределах доски."""
        return 0 <= row < ROWS and 0 <= col < COLS

    def get_checker_at(self, row, col):
        """Возвращает шашку на указанной позиции, если она есть."""
        for checker in self.checkers:
            if checker.row == row and checker.col == col:
                return checker
        return None

    def switch_turn(self):
        """Меняет ход на другого игрока."""
        self.current_color = MOVE_WHITE if self.current_color == MOVE_BLACK else MOVE_BLACK

    def check_end_game(self):
        """Проверяет, остались ли шашки только одного цвета."""
        white_exists = any(checker.color == "W" for checker in self.checkers)
        black_exists = any(checker.color == "B" for checker in self.checkers)

        if not white_exists:
            self.result_game = WIN_BLACK
            return True
        elif not black_exists:
            self.result_game = WIN_WHITE
            return True

        # Проверка на ничью: отсутствие допустимых ходов
        if not self.any_valid_moves(self.current_color) or len(self.checkers) <= 2:
            self.result_game = DRAW
            return True
        return False

    def any_valid_moves(self, color):
        """
        Проверяет, есть ли у шашек данного цвета хотя бы один допустимый ход.
        """
        for checker in self.checkers:
            if checker.color == color:
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.get_valid_moves(checker):
                            return True
        return False
