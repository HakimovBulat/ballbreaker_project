import os
import sys
import pygame


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


class Platfotm(pygame.sprite.Sprite):
    image_platform = load_image("platform.png", 1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platfotm.image_platform
        self.rect = self.image.get_rect()
        self.move = 'STOP'

        self.rect.x = 250
        self.rect.y = 450
        self.rect.width = 100
        self.rect.height = 10
        
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
            self.rect.x -= 2
        elif self.move == 'RIGHT':
            self.rect.x += 2

Platfotm(all_sprites)
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    running = True
    ball_pos = 300, 250

    v = 100
    fps = 150
    clock = pygame.time.Clock()
    move = 'left_up'

    while running:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, 'white', ball_pos, 10)
        #v += 10
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if move == 'left_up':
            ball_pos = ball_pos[0] - v / fps, ball_pos[1] - v / fps
        elif move == 'right_up':
            ball_pos = ball_pos[0] + v / fps, ball_pos[1] - v / fps
        elif move == 'left_down':
            ball_pos = ball_pos[0] - v / fps, ball_pos[1] + v / fps
        elif move == 'right_down':
            ball_pos = ball_pos[0] + v / fps, ball_pos[1] + v / fps
        pygame.draw.circle(screen, 'white', ball_pos, 10)

        if ball_pos[0] <= 10:
            if move == 'left_up':
                move = 'right_up'
            else:
                move = 'right_down'
        elif ball_pos[0] >= size[0] - 10:
            if move == 'right_up':
                move = 'left_up'
            else:
                move = 'left_down'
        elif ball_pos[1] <= 10:
            if move == 'right_up':
                move = 'right_down'
            else:
                move = 'left_down'
        elif ball_pos[1] >= size[1] - 10:
            if move == 'left_down':
                move = 'left_up'
            else:
                move = 'right_up'
        all_sprites.draw(screen)
        all_sprites.update(event)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
