import pygame

import Const


class Info:
    def __init__(self, screen):
        self.screen = screen
        self.info_font_move = pygame.font.SysFont("Times New Roman",28)
        self.end_font_move = pygame.font.SysFont("Times New Roman", 24)
        self.button_rect = pygame.Rect(620, 500, 135, 50)  # Координаты и размеры кнопки
        self.button_color = (200, 200, 200)
        self.button_hover_color = (170, 170, 170)

    def draw_info(self, checkers):
        # Отображение текущего игрока
        text = f"Ход: {'Белыx' if checkers.current_color == Const.MOVE_WHITE else 'Чёрныx'}"
        text_surface = self.info_font_move.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (620, 50))

        overall_result_text = "Победитель: "
        # Отрисовка общего результата
        if checkers.result_game is not None:
            if checkers.result_game == Const.DRAW:
                overall_result_text = "Результат: "
            overall_result_text += checkers.result_game
        else:
            overall_result_text += "-"
        overall_result_surface = self.info_font_move.render(overall_result_text, True, (0, 0, 0))
        self.screen.blit(overall_result_surface, (620, 180))

        # Отрисовка кнопки
        mouse_pos = pygame.mouse.get_pos()
        color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, color, self.button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect, 2)  # Рамка кнопки

        # Текст на кнопке
        button_text = self.end_font_move.render("Новая игра", True, (0, 0, 0))
        self.screen.blit(button_text, (self.button_rect.x + 10, self.button_rect.y + 5))

    def is_button_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return True
        return False
