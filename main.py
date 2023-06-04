import random

import pygame
from pygame.locals import *


WIDTH = 600  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 7 # частота кадров в секунду
SIZE = 30 # размер секции змейки

dir_dict = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': True}


class SnakeAI:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.display = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()
        self.fps = 6
        self.block_size = 30

        self.dx = 0
        self.dy = 0

        self.length = 1
        self.x = self.width / 2
        self.y = self.height / 2
        self.snake = [(self.x, self.y)]
        self.dir_dict = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': True}

        self.apple = random.randrange(0, self.width, self.block_size), random.randrange(0, self.height, self.block_size)



# x, y = random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE)
# apple = random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE)
# length = 1
# snake = [(x, y)]
# dx, dy = 0, 0

#pygame.mixer.init()  # для звука
#sc = pygame.display.set_mode([WIDTH, HEIGHT])
#clock = pygame.time.Clock()

# ball = pygame.image.load("wolv.png")
# rect = ball.get_rect()
# speed = [2, 2]

pygame.init()

snkai = SnakeAI()

running = True
while running:
    snkai.display.fill((0, 0, 0))

    if snkai.x < snkai.block_size and snkai.dx == -1:
        snkai.x = snkai.width
    elif snkai.x > snkai.width - 2 * snkai.block_size and snkai.dx == 1:
        snkai.x = -snkai.block_size
    elif snkai.y < snkai.block_size and snkai.dy == -1:
        snkai.y = snkai.height
    elif snkai.y > snkai.height - 2 * snkai.block_size and snkai.dy == 1:
        snkai.y = -snkai.block_size

    [(pygame.draw.rect(snkai.display, (0, 255, 0), (i + 2, j + 2, snkai.block_size - 4, snkai.block_size - 4))) for i, j in snkai.snake]
    pygame.draw.rect(snkai.display, (255, 0, 0), (snkai.apple[0] + 8, snkai.apple[1] + 8, snkai.block_size - 16, snkai.block_size - 16))

    snkai.x += snkai.dx * snkai.block_size
    snkai.y += snkai.dy * snkai.block_size
    snkai.snake.append((snkai.x, snkai.y))
    snkai.snake = snkai.snake[-snkai.length:]

    if snkai.snake[-1] == snkai.apple:
        while snkai.apple in snkai.snake:
            snkai.apple = random.randrange(0, snkai.width, snkai.block_size), random.randrange(0, snkai.height, snkai.block_size)

        snkai.length += 1
        #FPS += 0.1

    if (snkai.x, snkai.y) in snkai.snake[:-1]:
        running = False

    pygame.display.flip()
    snkai.clock.tick(int(snkai.fps))

    key_event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == KEYDOWN:
            key_event = event

    if key_event:
        if key_event.type == KEYDOWN:
            if key_event.key == 119 and dir_dict['UP']:
                snkai.dx, snkai.dy = 0, -1
                snkai.dir_dict = {'UP': True, 'DOWN': False, 'LEFT': True, 'RIGHT': True}
            if key_event.key == 115 and dir_dict['DOWN']:
                snkai.dx, snkai.dy = 0, 1
                snkai.dir_dict = {'UP': False, 'DOWN': True, 'LEFT': True, 'RIGHT': True}
            if key_event.key == 97 and dir_dict['LEFT']:
                snkai.dx, snkai.dy = -1, 0
                snkai.dir_dict = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': False}
            if key_event.key == 100 and dir_dict['RIGHT']:
                snkai.dx, snkai.dy = 1, 0
                snkai.dir_dict = {'UP': True, 'DOWN': True, 'LEFT': False, 'RIGHT': True}

    #key = pygame.key.get_pressed()


pygame.quit()