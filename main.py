import random

import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def init(self):
        pygame.sprite.Sprite.init(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)


WIDTH = 600  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 7 # частота кадров в секунду
SIZE = 40 # размер секции змейки

x, y = random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE)
apple = random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE)
length = 1
snake = [(x, y)]
dx, dy = 0, 0

pygame.init()
pygame.mixer.init()  # для звука
sc = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

ball = pygame.image.load("wolv.png")
rect = ball.get_rect()
speed = [2, 2]

dir_dict = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': True}

running = True
while running:
    sc.fill((0, 0, 0))

    if x < SIZE and dx == -1:
        x = WIDTH
    elif x > WIDTH - 2 * SIZE and dx == 1:
        x = -SIZE
    elif y < SIZE and dy == -1:
        y = HEIGHT
    elif y > HEIGHT - 2 * SIZE and dy == 1:
        y = -SIZE

    [(pygame.draw.rect(sc, (0, 255, 0), (i + 2, j + 2, SIZE - 4, SIZE - 4))) for i, j in snake]
    pygame.draw.rect(sc, (255, 0, 0), (apple[0] + 8, apple[1] + 8, SIZE - 16, SIZE - 16))

    x += dx * SIZE
    y += dy * SIZE
    snake.append((x, y))
    snake = snake[-length:]

    if snake[-1] == apple:
        while apple in snake:
            apple = random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE)

        length += 1
        #FPS += 0.1

    if (x, y) in snake[:-1]:
        running = False

    pygame.display.flip()
    clock.tick(int(FPS))

    key_event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == KEYDOWN:
            key_event = event

    if key_event:
        if key_event.type == KEYDOWN:
            if key_event.key == 119 and dir_dict['UP']:
                dx, dy = 0, -1
                dir_dict = {'UP': True, 'DOWN': False, 'LEFT': True, 'RIGHT': True}
            if key_event.key == 115 and dir_dict['DOWN']:
                dx, dy = 0, 1
                dir_dict = {'UP': False, 'DOWN': True, 'LEFT': True, 'RIGHT': True}
            if key_event.key == 97 and dir_dict['LEFT']:
                dx, dy = -1, 0
                dir_dict = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': False}
            if key_event.key == 100 and dir_dict['RIGHT']:
                dx, dy = 1, 0
                dir_dict = {'UP': True, 'DOWN': True, 'LEFT': False, 'RIGHT': True}

    #key = pygame.key.get_pressed()


pygame.quit()