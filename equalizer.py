import numpy as np
import pygame
from signals import SignalProcessor
import sys

WIDTH = 1200
HEIGHT = 600


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color_off, color_on, size, value_to_display):
        pygame.sprite.Sprite.__init__(self)

        self.color_off = color_off
        self.color_on = color_on

        self.value_to_display = value_to_display

        self.image = pygame.Surface((size[0], size[1]))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.image.fill(color_off)

    def update(self, *args):
        if args[0] >= self.value_to_display:
            self.image.fill(self.color_on)
        else:
            self.image.fill(self.color_off)


def generate_group(x: int, y: int, color_off, color_on, size, step, max_value, n_rows: int):
    group = pygame.sprite.Group()
    epsilon = 1e-1

    for i in range(n_rows):
        current_value = max_value - (max_value * (i + 1)) / n_rows + epsilon
        new_x, new_y = x, y + i * step
        group.add(Square(new_x, new_y, color_off, color_on, size, current_value))

    return group


def calculate_square_params(window_size, n_rows, n_ranges):
    width, height = window_size[0], window_size[1]
    calc_x, calc_y = width // (6 * n_ranges - 1), height // (3 * n_rows - 1)
    size = (5 * calc_x, 2 * calc_y)
    step = (6 * calc_x, 3 * calc_y)

    return size, step


def generate_groups(window_size, color_off, color_on, max_value, n_rows, n_ranges):
    size, step = calculate_square_params(window_size, n_rows, n_ranges)

    groups = []
    for i in range(n_ranges):
        group = generate_group(i * step[0], 0, color_off, color_on, size, step[1], max_value, n_rows)
        groups.append(group)

    return groups


def find_max_in_frequency_ranges(frequency_ranges, spectrum):
    n = len(frequency_ranges)

    max_elements = np.zeros(n)

    for i in range(n - 1):
        start_index = frequency_ranges[i]
        end_index = frequency_ranges[i + 1]

        max_elements[i] = np.max(spectrum[start_index:end_index])

    start_index = int(frequency_ranges[n - 1])
    max_elements[n - 1] = np.max(spectrum[start_index:])

    return max_elements


def run():
    interval = 4410
    sample_rate = 44100
    sound_recorder = SignalProcessor(sample_rate)
    sound_recorder.set_default_signal(interval)

    max_value = 5
    n_rows = 16

    ranges = [0, 2, 6, 10, 15, 20, 30, 45, 60, 80, 100, 130, 160, 200, 220, 250, 320, 400, 500, 650, 800, 1000, 1300,
              1600, 2000]
    n_ranges = len(ranges)

    pygame.init()

    background = (159, 193, 219)
    color_off = (255, 0, 0)
    color_on = (0, 155, 0)

    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    sc.fill(background)

    drawing_x = WIDTH // 10
    drawing_y = HEIGHT // 10

    drawing_size = (WIDTH - 2 * drawing_x, HEIGHT - 2 * drawing_y)

    drawing_surf = pygame.Surface(drawing_size)
    sc.blit(drawing_surf, (drawing_x, drawing_y))
    drawing_surf.fill('black')

    squares_surf_size = (drawing_size[0] - 2 * drawing_size[0] // 10, drawing_size[1] - 2 * drawing_size[1] // 10)
    squares_surf = pygame.Surface(squares_surf_size)
    drawing_surf.blit(squares_surf, (drawing_size[0] // 10, drawing_size[1] // 10))
    squares_surf.fill((10, 23, 38))

    clock = pygame.time.Clock()

    groups = generate_groups(squares_surf_size, color_off, color_on, max_value, n_rows, n_ranges)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        sc.blit(drawing_surf, (drawing_x, drawing_y))
        pygame.draw.rect(drawing_surf, (10, 23, 38), (0, 0, drawing_size[0], drawing_size[1]),
                         width=0, border_radius=15)
        pygame.draw.rect(drawing_surf, (87, 39, 38), (0, 0, drawing_size[0], drawing_size[1]),
                         width=5, border_radius=15)

        drawing_surf.blit(squares_surf, (drawing_size[0] // 10, drawing_size[1] // 10))

        sound_recorder.update_signal(interval // 4)
        sound_recorder.fft_signal(interval, output_type='linear')

        # print(sound_recorder.fft_data)

        for i in range(len(groups)):
            groups[i].draw(squares_surf)

        arr = find_max_in_frequency_ranges(ranges, sound_recorder.fft_data)

        pygame.display.update()
        for i in range(len(groups)):
            groups[i].update(arr[i])

        clock.tick(144)
