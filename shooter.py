#Створи власний Шутер!
from pygame import *
from random import randint

mixer.init()
font.init()
mixer.music.load('space.ogg')
#mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'spaceship.png'

lost = 0
count = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
                  
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        b = Bullet('bullet.png', self.rect.centerx - 7, self.rect.y, 15, 20, 15)
        bullets.add(b)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost +1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption('Shooter')
icon_image = image.load('ufo.png')
display.set_icon(icon_image)
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 300, win_height - 150, 80, 100, 10)

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    rand_x = randint(0, win_width - 100)
    rand_v = randint(3,8)
    rand_y = randint(-300, -50)
    nlo = Enemy('ufo.png', rand_x, -100 , 80, 50, 10)
    monsters.add(nlo)

finish =False
run = True

font1 = font.SysFont('Impact', 70)
font2 = font.SysFont('Impact', 30)
score = 0
score_text = font2.render('Рахунок:' + str(score), True, (255, 0, 0))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            lose = font1.render('You LOSE!', True, (255, 0, 0))


        collides = sprite.groupcollide(bullets, monsters, True, True)


        for c in collides:
            score+=1
            score_text = font2.render('Рахунок:' + str(score), True, (255, 0, 0))

        if score >= 3:
            finish = True
            lose = font1.render('You WIN!', True, (255, 0, 0))
            window.blit(lose, (win_width/2 - 100, win_height/2 - 50))

        window.blit(score_text, (20, 20))

        if finish:
            
            window.blit(lose, (win_width/2 - 100, win_height/2 - 50))
        bullets.draw(window)
        ship.reset()
        display.update()
    time.delay(50)