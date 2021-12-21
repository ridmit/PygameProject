import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 0
        self.top = 0
        self.cell_size = 100

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x, y = self.left, self.top
        size = self.cell_size
        for col in range(self.width):
            for row in range(self.height):
                pygame.draw.rect(screen, "white",
                                 (x + col * size, y + row * size, size, size),
                                 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos

        min_x = self.left
        max_x = self.left + self.cell_size * self.width

        min_y = self.top
        max_y = self.top + self.cell_size * self.height

        if min_x <= x <= max_x and min_y <= y <= max_y:
            cur_x = (x - min_x) // self.cell_size
            cur_y = (y - min_y) // self.cell_size
            return cur_x, cur_y
        return

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
