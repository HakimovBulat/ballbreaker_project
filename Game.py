import os
import sys
import pygame
from Sprites import *
from Camera import Camera

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


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


def win_screen(level):
    boom = AnimatedSprite(load_image("boom.png"), 9, 9, 100, 100)
    clock = pygame.time.Clock()
    while True:
        intro_text = [
            "Вы прошли уровень " + level + '!', "", "", "", "", 
            "", "", "", "Пробел - продолжить игру", "", "Escape - выйти"
                      ]
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    terminate()
        for sprite in all_sprites:
            if sprite != boom:
                sprite.kill()
        all_sprites.draw(screen)
        boom.update()
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

Border(0, 0, WIDTH, 0)
Border(0, HEIGHT, WIDTH, HEIGHT)
Border(0, 0, 0, HEIGHT)
Border(WIDTH, 0, WIDTH, HEIGHT)

platform = Platfotm(all_sprites)
ball = Ball(all_sprites)
for i in range(5):
    for j in range(6):
        Brick(30 + 81 * j, 20 + 31 * i, 80, 30)
camera = Camera()
#for i in range(1):
#    Brick(300, 20 + 31 * i, 80, 30)


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
            for hit in hits:
                create_particles(hit.rect.center)
        camera.update(ball); 
        for sprite in all_sprites:
              camera.apply(sprite)
        clock.tick(FPS)
        pygame.display.flip()
        if not bricks_group:
            win_screen("1")
    pygame.quit()