import numpy as np
import pygame
# import numpy as np
from signals import *
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


def generate_squares_group(x: int, n: int, color_on, color_off, size, max_value, group):
    for i in range(n):
        group.add(Square(x, 30 + 40 * i, color_on, color_off, size, max_value - (max_value * (i + 1)) / n))


def find_max_in_frequency_ranges(frequency_ranges, spectrum, sample_rate):
    n = len(frequency_ranges)
    interval = spectrum.shape[0]

    max_elements = np.zeros(n)

    for i in range(len(frequency_ranges) - 1):
        start_index = int(frequency_ranges[i] * interval / sample_rate)
        end_index = int(frequency_ranges[i + 1] * interval / sample_rate)

        max_elements[i] = np.max(spectrum[start_index:end_index])

    start_index = int(frequency_ranges[n - 1] * interval / sample_rate)
    max_elements[n - 1] = np.max(spectrum[start_index:])

    return max_elements


if __name__ == '__main__':
    interval = 4410
    sample_rate = 44100
    ranges = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 12000, 16000]

    pygame.init()

    squares_range_1 = pygame.sprite.Group()
    squares_range_2 = pygame.sprite.Group()
    squares_range_3 = pygame.sprite.Group()
    squares_range_4 = pygame.sprite.Group()
    squares_range_5 = pygame.sprite.Group()
    squares_range_6 = pygame.sprite.Group()
    squares_range_7 = pygame.sprite.Group()
    squares_range_8 = pygame.sprite.Group()
    squares_range_9 = pygame.sprite.Group()
    squares_range_10 = pygame.sprite.Group()
    squares_range_11 = pygame.sprite.Group()

    generate_squares_group(100, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_1)
    generate_squares_group(140, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_2)
    generate_squares_group(180, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_3)
    generate_squares_group(220, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_4)
    generate_squares_group(260, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_5)
    generate_squares_group(300, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_6)
    generate_squares_group(340, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_7)
    generate_squares_group(380, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_8)
    generate_squares_group(420, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_9)
    generate_squares_group(460, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_10)
    generate_squares_group(500, 10, (0, 155, 0), (255, 0, 0), (30, 30), 7, squares_range_11)

    sc = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    sound = np.zeros(interval)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        sound_fft = signal_fft(sound, interval)

        arr = find_max_in_frequency_ranges(ranges, sound_fft, sample_rate)
        # print(arr)

        new_interval = interval // 4
        new_sound = record_signal(new_interval / sample_rate, sample_rate)

        sound = sound[new_interval:]
        sound = np.append(sound, new_sound)

        sc.fill((0, 0, 0))
        squares_range_1.draw(sc)
        squares_range_2.draw(sc)
        squares_range_3.draw(sc)
        squares_range_4.draw(sc)
        squares_range_5.draw(sc)
        squares_range_6.draw(sc)
        squares_range_7.draw(sc)
        squares_range_8.draw(sc)
        squares_range_9.draw(sc)
        squares_range_10.draw(sc)
        squares_range_11.draw(sc)

        # value_coordinate += 1 / (5 * np.pi)
        value = arr[0]

        pygame.display.update()

        clock.tick(144)

        squares_range_1.update(arr[0])
        squares_range_2.update(arr[1])
        squares_range_3.update(arr[2])
        squares_range_4.update(arr[3])
        squares_range_5.update(arr[4])
        squares_range_6.update(arr[5])
        squares_range_7.update(arr[6])
        squares_range_8.update(arr[7])
        squares_range_9.update(arr[8])
        squares_range_10.update(arr[9])
        squares_range_11.update(arr[10])
