import os
import sys
import pygame
from random import sample

pygame.init()
size = WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


player = None
FPS = 50
V = 200


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["                            Ballbreaker", "",
                  "Правила игры:",
                  "Разбей все кирпичики белым шаром,",
                  "используя платформу, передвигающуюся с",
                  "помощью клавиш <- и ->.", "", "", "Пробел - начать игру",
                      "", "Escape - выйти"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def level_screen(level):
    fon = pygame.transform.scale(load_image(level), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == MYEVENTTYPE:
                return
        pygame.display.flip()
        clock.tick(FPS)
    

level_screen('first_level.png')
all_sprites = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

class Platfotm(pygame.sprite.Sprite):
    image_platform = load_image("platform.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platfotm.image_platform
        self.rect = self.image.get_rect()
        self.move = 'STOP'
        self.rect.x = 250
        self.rect.y = 450
        
    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_LEFT:
                self.move = 'LEFT'
            elif args[0].key == pygame.K_RIGHT:
                self.move = 'RIGHT'
        elif args[0].type == pygame.KEYUP:
            if args[0].key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.move = 'STOP'

        if self.move == 'LEFT':
            self.rect.x -= 10
        elif self.move == 'RIGHT':
            self.rect.x += 10
        
    def collideball(self, ball):
        if ball.rect.y + 20 == self.rect.y and self.rect.x <= ball.rect.x <= self.rect.x + 100:
            if ball.move == 'left_down':
                ball.move = 'left_up'
            else:
                ball.move = 'right_up'


class Ball(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"), (10, 10), 10)
        self.rect = pygame.Rect(300, 250, 20, 20)
        self.move = 'left_up'

    def update(self, *args):
        if self.move == 'left_up':
            self.rect.x, self.rect.y = self.rect.x - V / FPS, self.rect.y - V / FPS
        elif self.move == 'right_up':
            self.rect.x, self.rect.y = self.rect.x + V / FPS, self.rect.y - V / FPS
        elif self.move == 'left_down':
            self.rect.x, self.rect.y = self.rect.x - V / FPS, self.rect.y + V / FPS
        elif self.move == 'right_down':
            self.rect.x, self.rect.y = self.rect.x + V / FPS, self.rect.y + V / FPS

        if self.rect.x <= 1:
            if self.move == 'left_up':
                self.move = 'right_up'
            else:
                self.move = 'right_down'
        elif self.rect.x >= size[0] - 20:
            if self.move == 'right_up':
                self.move = 'left_up'
            else:
                self.move = 'left_down'
        elif self.rect.y <= 1:
            if self.move == 'right_up':
                self.move = 'right_down'
            else:
                self.move = 'left_down'
        elif self.rect.y >= size[1] - 20:
            if self.move == 'left_down':
                self.move = 'left_up'
            else:
                self.move = 'right_up'

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(all_sprites)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, tuple(sample(range(10, 255, 1), 3)), (x, y, width, height), 0)
        self.rect = pygame.Rect(x, y, width, height)
        self.move = 'left_up'
        bricks_group.add(self)


platform = Platfotm(all_sprites)
ball = Ball(all_sprites)
for i in range(5):
    for j in range(6):
        Brick(30 + 40 * j, 20 + 15 * i, 80, 30)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        platform.collideball(ball)
        all_sprites.draw(screen)
        all_sprites.update(event)
        hits = pygame.sprite.spritecollide(ball, bricks_group, True)
        if hits:
            if ball.move == 'left_down':
                ball.move = 'left_up'
            elif ball.move == 'right_down':
                ball.move = 'right_up'
            elif ball.move == 'left_up':
                ball.move = 'left_down'
            elif ball.move == 'right_up':
                ball.move = 'right_down'
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
