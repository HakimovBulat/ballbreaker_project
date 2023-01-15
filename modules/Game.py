import sys
import pygame
from modules.Sprites import *
from modules.Camera import Camera


class Game:
    def __init__(self):
        self.start_screen()
    
    def create_particles(seelf, position):
        particle_count = 20
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, choice(numbers), choice(numbers))

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        pygame.display.set_caption('')
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
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
            pygame.display.flip()
            clock.tick(FPS)

    def win_screen(self, level):
        boom = AnimatedSprite(load_image("boom.png"), 9, 9, 100, 100)
        pygame.display.set_caption('Порадуйтесь!')
        clock = pygame.time.Clock()
        while True:
            intro_text = [
                "Вы прошли " + level + '!', "", "", "", "", 
                "", "",  "Пробел - продолжить игру", "", "Escape - выйти"
                ]
            if level == 'всю игру':
                intro_text = [
                    "Вы прошли " + level + '!', "", "", "", "", 
                    "", "",  "Пробел - начать игру сначала", "", "Escape - выйти"
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
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        boom.kill()
                        if level == 'всю игру':
                            self.game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        self.terminate()
    
            all_sprites.draw(screen)
            boom.update()
            pygame.display.flip()
            clock.tick(FPS)

    def lose_screen(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption('Не расстраивайтесь!')
        pygame.mixer.music.load('sounds/sound_lose.mp3')
        pygame.mixer.music.play()
        while True:
            intro_text = [
                "Вы проиграли!", "", "", "", "", 
                "", "",  "Пробел - начать игру сначала", "", "Escape - выйти"
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
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.pause()
                        self.game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        self.terminate()
            pygame.display.flip()
            clock.tick(FPS)

    def level_screen(self, level):
        pygame.display.set_caption('')
        fon = pygame.transform.scale(load_image(level), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        clock = pygame.time.Clock()
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == MYEVENTTYPE:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    def level1(self):
        self.level_screen('first_level.png')

        Border(0, 0, WIDTH, 0)
        Border(0, HEIGHT, WIDTH, HEIGHT)
        Border(-1, 0, -1, HEIGHT)
        Border(WIDTH, 0, WIDTH, HEIGHT)
        platform = Platfotm()
        ball = Ball()
        for i in range(5):
            for j in range(6):
                Brick(30 + 81 * j, 20 + 31 * i, 80, 30)

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
            platform.collideball_fast(ball)
            all_sprites.draw(screen)
            all_sprites.update(event)
            hits = pygame.sprite.spritecollide(ball, bricks_group, True)
            if hits:
                for hit in hits:
                    self.create_particles(hit.rect.center)

            clock.tick(FPS)
            pygame.display.flip()

            if not bricks_group:
                for sprite in all_sprites:
                    sprite.kill()
                self.win_screen("1 уровень")
                return True
            if ball.rect.y > platform.rect.y:
                for sprite in all_sprites:
                    sprite.kill()
                self.lose_screen()
                return False
            pygame.display.flip()
        pygame.quit()

    def level2(self):
        self.level_screen('second_level.png')

        Border(0, 0, WIDTH, 0)
        Border(0, HEIGHT, WIDTH, HEIGHT)
        Border(-1, 0, -1, HEIGHT)
        Border(WIDTH, 0, WIDTH, HEIGHT)
        platform = Platfotm()
        ball = Ball()
        for i in range(5):
            for j in range(6):
                Brick(30 + 81 * j, 20 + 31 * i, 80, 30)
        camera = Camera()

        pygame.init()
        pygame.display.set_caption('Уровень 2')
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
                    self.create_particles(hit.rect.center)
            camera.update(ball); 
            for sprite in all_sprites:
                camera.apply(sprite)
            
            clock.tick(FPS)
            pygame.display.flip()
            if not bricks_group:
                for sprite in all_sprites:
                    sprite.kill()
                self.win_screen("2 уровень")
                return True
            if ball.rect.y > platform.rect.y:
                for sprite in all_sprites:
                    sprite.kill()
                self.lose_screen()
                return False
            pygame.display.flip()
        pygame.quit()
    
    def level3(self):
        self.level_screen('third_level.png')
        
        Border(0, 0, WIDTH, 0)
        Border(0, HEIGHT, WIDTH, HEIGHT)
        Border(-1, 0, -1, HEIGHT)
        Border(WIDTH, 0, WIDTH, HEIGHT)
        platform = Platfotm()
        ball = Ball()
        fake_ball1 = Ball(x=randint(50, 450), y=randint(50, 450), vx = randint(-2, 3), vy = randint(-2, 3))
        fake_ball2 = Ball(x=randint(50, 450), y=randint(50, 450), vx = randint(-2, 3), vy = randint(-2, 3))
        fake_ball3 = Ball(x=randint(50, 450), y=randint(50, 450), vx = randint(-2, 3), vy = randint(-2, 3))
        for i in range(5):
            for j in range(6):
                Brick(30 + 81 * j, 20 + 31 * i, 80, 30)

        pygame.init()
        pygame.display.set_caption('Уровень 3')
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
                    self.create_particles(hit.rect.center)
            clock.tick(FPS)
            pygame.display.flip()

            if not bricks_group:
                for sprite in all_sprites:
                    sprite.kill()
                pygame.mixer.music.load('sounds/sound_win.mp3')
                pygame.mixer.music.play()
                self.win_screen("всю игру")
                return True
            if ball.rect.y > platform.rect.y:
                for sprite in all_sprites:
                    sprite.kill()
                self.lose_screen()
                return False
            pygame.display.flip()
        pygame.quit()

    def game(self):
        if self.level1():
            if self.level2():
                if self.level3():
                    return 