import pygame

from Const import *
import Board
import Checkers
import Info


class ClassGameCheckers:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH-190, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("Шашки Апид Содок")

        # Инициализация компонентов игры
        self.board = Board.ClassBoard(self.screen)
        self.checkers = Checkers.ClassChecker(self.screen)
        self.info = Info.Info(self.screen)

    def run_game(self):
        while self.running:
            self.handle_events()
            self.render()
            self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.info.is_button_clicked(event):
                self.checkers.initialize_checkers()
            self.checkers.handle_events(event)

    def render(self):
        self.screen.fill(WHITE)
        self.board.draw_board()
        self.checkers.draw_checkers()
        self.info.draw_info(self.checkers)
        pygame.display.flip()

    def check_game_over(self):
        if self.checkers.check_end_game():
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Пользователь закрыл окно
                        self.running = False
                        return
                    if self.info.is_button_clicked(event):
                        self.checkers.initialize_checkers()
                        self.running = True
                        return
                self.render()                      # Отрисовываем результаты на экране
                pygame.display.flip()
                self.clock.tick(10)                # Ограничиваем частоту кадров до 10 FPS

