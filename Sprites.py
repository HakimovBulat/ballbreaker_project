import pygame
import os
from random import sample, choice, randint, randrange

pygame.init()
size = WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode(size)
player = None
FPS = 50
V = 200

all_sprites = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


class Platfotm(pygame.sprite.Sprite):
    image_platform = load_image("platform.png")

    def __init__(self):
        super().__init__(all_sprites)
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
            if self.rect.x > 0:
                self.rect.x -= 10
        elif self.move == 'RIGHT':
            if self.rect.x < 500:
                self.rect.x += 10
        
    def collideball(self, ball):
        if ball.rect.y + 20 == self.rect.y and self.rect.x <= ball.rect.x <= self.rect.x + 100:
            ball.vx = ball.vx
            ball.vy = -ball.vy
    
    def collideball_fast(self, ball):
        if ball.rect.y + 20 == self.rect.y and self.rect.x <= ball.rect.x <= self.rect.x + 100:
            ball.vx = ball.vx + 1
            ball.vy = -(ball.vy + 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=300, y=250, color=(255, 255, 255)):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.vx = 4
        self.vy = 4

    def update(self, *args):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, bricks_group):
            self.vx = self.vx
            self.vy = -self.vy


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(all_sprites)
        self.image = pygame.Surface((width, height))
        self.image.fill(tuple(sample(range(10, 255, 1), 3)))
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        bricks_group.add(self)


screen_rect = (0, 0, WIDTH, HEIGHT)


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1
        particles_group.add(self)

    def update(self, *args):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((255, 255, 255))