import pygame
import time
import random


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
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

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


class Enemy:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.rect = self.img.get_rect(center=(self.x, self.y))

        self.done = False

    def draw(self, win):
        win.blit(self.img, self.rect)

    def update(self, player):
        global score

        self.rect.y += 1

        for bullet in player.bullets:
            if self.rect.colliderect(bullet.surf.get_rect(center=(bullet.x, bullet.y))):
                self.done = True

        if self.rect.y > 720:
            self.done = True
            score -= 2


screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Space Invaders")

player = Player(1280 // 2, 650, screen)

clock = pygame.time.Clock()

background_sound = pygame.mixer.Sound("./bg_music.mp3")

background_sound.play(-1)

enemys = []

enemy_delay = 2
end_time = time.time()

enemy_imgs = [pygame.image.load("./enemy.svg"), pygame.image.load('./enemy2.png')]

font = pygame.font.SysFont("cosmicsans", 34)
score = 0
score_text = font.render(f"Score: {score}", True, (255, 255, 255))

stage = 'play'

win_screen = pygame.transform.scale(pygame.image.load('./win.png'), (1280, 720))

while True:
    clock.tick(60)

    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if stage == 'play':
        player.update()
        player.draw()

        for enemy in enemys:
            if enemy.done:
                enemys.remove(enemy)
                score += 1
                enemy_delay -= 0.01
                continue

            enemy.update(player)
            enemy.draw(screen)

        if time.time() >= end_time:
            enemys.append(
                Enemy(
                    random.randint(0, 1200),
                    100,
                    pygame.transform.scale(random.choice(enemy_imgs), (60, 60)),
                )
            )
            end_time = time.time() + enemy_delay

        screen.blit(score_text, (100, 100))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))

        if score < 0:
            pygame.quit()
            exit("You lose, score: " + str(score))
        if score > 20:
            stage = 'win'
    else:
        screen.blit(win_screen, (0, 0))

    pygame.display.update()
