from pygame import *
from random import randint
import time as timer

Levels = {
    1 : [3, 1, 2],
    2 : [5, 2, 3]
}

current_level = 1
ENEMIES_NUM = Levels[current_level][0]
ASTEROIDS_NUM = Levels[current_level][1]
RELOADING_TIME = Levels[current_level][2]

window = display.set_mode((700, 500))
clock = time.Clock()
display.set_caption('Space Fighter')
mixer.init()
font.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.01)
mixer.music.play(-1)
fart = mixer.Sound('fire.ogg')
fart.set_volume(0.02)
skipped = 0
destroyed = 0
counter_bullets = 0
timers = timer.time()
font1 = font.SysFont('Arial', 30)

background = transform.scale(
    image.load("galaxy.jpg"),
    (700, 500)
)
skipped_font = font1.render(
    'Пропущено: ' + str(skipped), False, (255, 255, 255)
)
destroyed_font = font1.render(
    'Счёт: ' + str(destroyed), False, (255, 255, 255)
)
win = font1.render(
    'YOU WIN!', True, (255, 215, 0)
)
loss = font1.render(
    'YOU LOSE!', True, (255, 0, 0)
)
reloading_font = font1.render(
    'Перезарядка: '+ str(RELOADING_TIME - int(timer.time() - timers)), True, (255, 255, 255)
)

class GameSprite(sprite.Sprite):
    def __init__(self, speed, p_image, x, y, scale_x, scale_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (scale_x, scale_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullets.add(
            Bullet(10, 'bullet.png', self.rect.centerx, self.rect.top, 10, 20)
        )
        fart.play()

class Enemy(GameSprite):
    def update(self):
        global skipped, skipped_font
        self.rect.y += self.speed
        if self.rect.y >= 400:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            skipped += 1
            skipped_font = font1.render(
                'Пропущено: ' + str(skipped), True, (255, 255, 255)
            )

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 400:
            self.rect.y = 0
            self.rect.x = randint(100, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -10:
            self.kill()

monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

galaxy_ship = Player(7, 'rocket.png', 350, 400, 90, 100)

game = True
finish = False
reloading = False
while game:
    window.blit(background,(0, 0))
    if reloading:
        reloading_font = font1.render(
            'Перезарядка: '+ str(RELOADING_TIME - int(timer.time() - timers)), True, (255, 255, 255)
            )
        window.blit(reloading_font, (280, 470))
        if timer.time() - timers >= RELOADING_TIME:
            reloading = False
            counter_bullets = 0
    for i in range(ENEMIES_NUM):
        if len(monsters) < ENEMIES_NUM:
            monsters.add(Enemy(randint(1,2), 'ufo.png', randint(100, 600), 0, 80, 50))
    for i in range(ENEMIES_NUM):
        if len(asteroids) < ASTEROIDS_NUM:
            asteroids.add(Asteroid(randint(1,2), 'asteroid.png', randint(100, 600), 0, 80, 50))        
    for e in event.get():
        if e.type == QUIT:
            game = False
        if counter_bullets < 5 and reloading == False:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    counter_bullets += 1
                    galaxy_ship.fire()
                    timers = timer.time()
        else:
            reloading = True
    if finish != True:
        window.blit(skipped_font, (30, 60))
        window.blit(destroyed_font, (30, 30))
        galaxy_ship.draw()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        for m in monsters:
            if sprite.collide_rect(galaxy_ship, m):
                mixer.music.stop()
                window.blit(loss, (250, 250))
                finish = True
            for b in bullets:
                if sprite.collide_rect(m, b):
                    m.kill()
                    b.kill()
                    destroyed += 1
                    destroyed_font = font1.render(
                    'Счет: ' + str(destroyed), True, (255, 255, 255)
                    )
        if len(sprite.spritecollide(galaxy_ship, asteroids, False)) > 0:
            mixer.music.stop()
            window.blit(loss, (250, 250))
            finish = True
        sprite.groupcollide(bullets, asteroids, True, False)
        if skipped >= 3:
            mixer.music.stop()
            window.blit(loss, (250, 250))
            finish = True
        if destroyed >= 10 and current_level == 2:
            mixer.music.stop()
            window.blit(win, (250, 250))
            finish = True
        elif destroyed >= 5:
            current_level += 1
            skipped = 0
            destroyed = 0
        else:
            ENEMIES_NUM = Levels[current_level][0]
            ASTEROIDS_NUM = Levels[current_level][1]
            RELOADING_TIME = Levels[current_level][2]
        galaxy_ship.update()
        clock.tick(40)
        display.update()