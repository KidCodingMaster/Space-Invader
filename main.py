import pygame
import time


pygame.init()
pygame.mixer.init()


class Player:
    def __init__(self, x, y, win):
        self.x = x
        self.y = y

        self.img = pygame.transform.scale(pygame.image.load("./ufo.png"), (60, 30))
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.bullets = []

        self.win = win

        self.bullet_delay = 0.2
        self.end_time = time.time() + self.bullet_delay
        self.can_shoot = True

    def draw(self):
        self.win.blit(self.img, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2

        if keys[pygame.K_SPACE]:
            if self.can_shoot:
                self.bullets.append(Bullet(self))
                self.can_shoot = False
            else:
                if time.time() >= self.end_time:
                    self.can_shoot = True

                    self.end_time = time.time() + self.bullet_delay

        for bullet in self.bullets:
            bullet.draw()
            bullet.update()

            if bullet.done:
                self.bullets.remove(bullet)


class Bullet:
    def __init__(self, player):
        self.player = player

        self.surf = pygame.Surface((5, 15))
        self.surf.fill("white")

        self.x = self.player.rect.centerx
        self.y = self.player.rect.centery

        self.done = False

    def draw(self):
        self.player.win.blit(self.surf, (self.x, self.y))

    def update(self):
        self.y -= 3

        if self.y < 0:
            self.done = True


screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Space Invaders")

player = Player(1280 // 2, 650, screen)

clock = pygame.time.Clock()

background_sound = pygame.mixer.Sound("./bg_music.mp3")

background_sound.play(-1)

while True:
    clock.tick(60)

    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.update()
    player.draw()

    pygame.display.update()
