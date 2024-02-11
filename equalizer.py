import pygame
import numpy as np
import sys


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color_on, color_off, size, value_to_display):
        pygame.sprite.Sprite.__init__(self)

        self.color_on = color_on
        self.color_off = color_off

        self.value_to_display = value_to_display

        self.image = pygame.Surface((size[0], size[1]))
        self.rect = self.image.get_rect(center=(x, y))

        self.image.fill(color_off)

    def update(self, *args):
        if args[0] >= self.value_to_display:
            self.image.fill(self.color_on)
        else:
            self.image.fill(self.color_off)


def generate_squares_group(n: int, color_on, color_off, size, max_value, group):
    for i in range(n):
        group.add(Square(100, 30 + 40 * i, color_on, color_off, size, max_value - (max_value * (i + 1)) / n))


if __name__ == '__main__':
    pygame.init()

    squares = pygame.sprite.Group()

    generate_squares_group(10, (0, 155, 0), (255, 0, 0), (30, 30), 1, squares)

    sc = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # s1 = Square(100, 60, (0, 155, 0), (255, 0, 0), (30, 30), 0.7)
    # s2 = Square(100, 100, (0, 155, 0), (255, 0, 0), (30, 30), 0.5)
    # s3 = Square(100, 140, (0, 155, 0), (255, 0, 0), (30, 30), 0.3)

    value_coordinate = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        sc.fill((0, 0, 0))
        squares.draw(sc)

        value_coordinate += 1 / (5 * np.pi)
        value = np.sin(value_coordinate)

        pygame.display.update()

        clock.tick(60)

        squares.update(value)
