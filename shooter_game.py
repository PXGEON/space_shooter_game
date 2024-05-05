from pygame import *
from time import time as timer
from random import randint

win_width = 700
win_height = 500
x1 = win_height - 100
y1 = 400
x2 = randint(80, win_width - 80)
y2 = 0
speed = 1
clock = time.Clock()
FPS = 60
img_hero = "rocket.png"  # игрок
img_enemy = "ufo.png"  # враг
img_barrier = "asteroid.png"  # препятствие
img_bullet = "bullet.png"  # пуля


window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    # метод "выстрел"
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.x, self.rect.y, 10 )
        bullets.add(bullet)


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Barrier(GameSprite):
    def update(self):
        self.rect.y += self.speed  
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80)           
            self.rect.y = -50


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

            
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
player = transform.scale(image.load("rocket.png"), (100, 100))
monster = transform.scale(image.load("ufo.png"), (150, 100))
bullet = transform.scale(image.load("bullet.png"), (20, 20))
asteroid = transform.scale(image.load("asteroid.png"), (50, 50))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


player = Player(img_hero, x1, y1, 7)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 2)
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Barrier(img_barrier, randint(0, win_width - 50), randint(1, 4), 3 )
    asteroids.add(asteroid)


score = 0  # счетчик сбитых
lost = 0  # счетчик пропущенных
max_lost = 5  # максимум пропущенных
max_score = 15  # количество очков для победы


font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render("YOU WIN!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!", True, (180, 0, 0))

finish = False
#Игровой цикл
game = True
while game:  

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    fire_sound.play()  
                    player.fire() 

    if finish != True:
        window.blit(background, (0, 0)) 

        text = font1.render("Счет: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        player.update()  
        monsters.update()  
        bullets.update()
        asteroids.update()  

        player.reset()  
        monsters.draw(window)  
        bullets.draw(window)
        asteroids.draw(window)  

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False
        ):
            sprite.spritecollide(player, asteroids, True)
            finish = True
            window.blit(lose, (200, 200))  # выводим надпись о проигрыше


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1  # добавляем 1 очко
            
        if  lost >= max_lost:
            finish = True  # завершаем игру
            window.blit(lose, (200, 200))  # выводим надпись о проигрыше

        if score >= max_score:
            finish = True  # завершаем игру
            window.blit(win, (200, 200))  # выводим надпись о выигрыше

    display.update()
    clock.tick(FPS)

