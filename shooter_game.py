from pygame import *
from random import*

score = 0
lost = 0
font.init()
font2 = font.SysFont("Arial", 30)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 6, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    #движение пули
    def update(self):
        self.rect.y -= self.speed
        global lost
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
rocket = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
   monster = Enemy("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)


run = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.SysFont("Arial", 70)
win = font.render('YOU WIN!', True, (180, 0, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    if not finish:
        window.blit(galaxy, (0,0))
        text = font2.render("Счёт:" + str(score), 1, (225, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        rocket.update()
        rocket.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

    #проверка столкновения пули с монстром
    colliders = sprite.groupcollide(monsters, bullets, True, True)
    for c in colliders:
        score = score + 1
        monster = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)

    #ситуация проигрыша
    sprite_list = sprite.spritecollide(rocket, monsters, False)
    if lost > 20 or sprite_list:
        finish = True
        window.blit(lose, (200, 200))

    #ситуация выйгрыша
    if score > 10 :
        finish = True
        window.blit(win, (200, 200))


    display.update()

    clock.tick(FPS)
    