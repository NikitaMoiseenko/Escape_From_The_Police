from pygame import *
from random import *

W = 1655
H = 1050
FPS = 60

#-----------------------------------

ENEMY_COUNT = 3

#--------

COIN_COUNT = 20

#-----------------------------------


window = display.set_mode((W, H))
timer = time.Clock()


#---------------------------------------------------------------------------------------


backgroud = transform.scale(image.load('road_pygame.jpg'), (W,H))

#---------------------------------------

game_over = transform.scale(image.load('game_over_pygame.jpg'), (W,H))

#---------------------------------------

game_win = transform.scale(image.load('game_win.jpg'), (W,H))


#---------------------------------------------------------------------------------------

mixer.init()

randomEnemies = []
coinList = []

#------------------------------------------------------------

class Sprite():
    def __init__(self, model, w, h, x, y):
        self.model = transform.scale(image.load(model), (w, h))
        self.rect = self.model.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.degree = 0

    def set_rotate(self, degree):
        dif = degree - self.degree
        self.degree = degree
        self.model = transform.rotate(self.model, dif)

    def draw(self):
        window.blit(self.model, (self.rect.x, self.rect.y))

class Chatacter(Sprite):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y)
        self.speed = speed
    def move(self, direction):
        if direction == 0 and self.rect.y > 0:
            for wall in wallList:
                if self.rect.y <= wall.rect.y + wall.rect.h  and self.rect.y >= wall.rect.y:
                    if (wall.rect.x + wall.rect.w >= self.rect.x >= wall.rect.x) or (wall.rect.x  >= self.rect.x + wall.rect.w  >= wall.rect.x + wall.rect.w ):
                       return
            self.rect.y -= self.speed
        if direction == 1 and self.rect.y < H - self.rect.h:
            for wall in wallList:
                if self.rect.y + self.rect.h  >= wall.rect.y and self.rect.y + self.rect.h  <= wall.rect.y + wall.rect.h :
                    if (wall.rect.x + wall.rect.w >= self.rect.x >= wall.rect.x) or (wall.rect.x  >= self.rect.x + wall.rect.w  >= wall.rect.x + wall.rect.w ):
                       return
            self.rect.y += self.speed
        if direction == 2 and self.rect.x > 0:
            for wall in wallList:
                if self.rect.x <= wall.rect.x + wall.rect.w  and self.rect.x >= wall.rect.x:
                    if (self.rect.y > wall.rect.y and self.rect.y < wall.rect.y + wall.rect.h) or (self.rect.y + self.rect.h > wall.rect.y and self.rect.y + self.rect.h < wall.rect.y + wall.rect.h):
                        return
            self.rect.x -= self.speed

        if direction == 3 and self.rect.x < W - self.rect.w:
            for wall in wallList:
                if self.rect.x + self.rect.w >= wall.rect.x and self.rect.x + self.rect.w <=  wall.rect.x + wall.rect.w:
                    if (self.rect.y > wall.rect.y and self.rect.y < wall.rect.y + wall.rect.h) or (self.rect.y + self.rect.h > wall.rect.y and self.rect.y + self.rect.h < wall.rect.y + wall.rect.h):
                        return
            self.rect.x += self.speed

class Player(Chatacter):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y, speed)

    def move(self):
        najatie_knopki = key.get_pressed()


     #-------------------------------------------------------------------

        if najatie_knopki[K_w]:
            self.set_rotate(90)
            super().move(0)

     #--------------------------------------------------------------------

        if najatie_knopki[K_s]:
            self.set_rotate(270)
            super().move(1)

     #--------------------------------------------------------------------

        if najatie_knopki[K_a]:
            self.set_rotate(180)
            super().move(2)

     #--------------------------------------------------------------------

        if najatie_knopki[K_d]:
            self.set_rotate(0)
            super().move(3)

     #--------------------------------------------------------------------

        if najatie_knopki[K_c]:
            mixer.music.pause()

     #--------------------------------------------------------------------

        if najatie_knopki[K_x]:
            mixer.music.unpause()

     #--------------------------------------------------------------------

        if najatie_knopki[K_1]:
            mixer.music.load('Driftin.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_2]:
            mixer.music.load('Grubby chase.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_3]:
            mixer.music.load('jake-hill-by-the-sword.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_4]:
            mixer.music.load('jake-hill-i-chose-violence-emptiness.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_5]:
            mixer.music.load('ovg! - Death Lotto.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_6]:
            mixer.music.load('Portwave_Shadow_Lady_PHONK_REMIX.mp3')
            mixer.music.play()

     #--------------------------------------------------------------------

        if najatie_knopki[K_LSHIFT] and najatie_knopki[K_w]:
            self.rect.y -= self.speed

     #--------------------------------------------------------------------

        if najatie_knopki[K_LSHIFT] and najatie_knopki[K_s]:
            self.rect.y += self.speed

     #--------------------------------------------------------------------

        if najatie_knopki[K_LSHIFT] and najatie_knopki[K_a]:
            self.rect.x -= self.speed

     #--------------------------------------------------------------------

        if najatie_knopki[K_LSHIFT] and najatie_knopki[K_d]:
            self.rect.x += self.speed

     #--------------------------------------------------------------------


    def checkCollison(self):
        if self.rect.colliderect(enemy.rect) == True:
            return True
        for e in randomEnemies:
            if self.rect.colliderect(e.rect) == True:
                return True
        return False

class Enemy(Chatacter):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y, speed)


    def chase(self, target):
        if target.rect.x > self.rect.x:
            super().move(3)
        else:
            super().move(2)
        if target.rect.y > self.rect.y:
            super().move(1)
        else:
            super().move(0)

    def move(self):
        direction = randint(0,3)
        super().move(direction)

class Coin(Sprite):
    def __init__(self, model, w, h, x, y):
        super().__init__(model, w, h, x, y)


    def checkCollison(self):
        if self.rect.colliderect(myPlayer.rect) == True:
            return True
        for p in randomEnemies:
            if self.rect.colliderect(p.rect) == True:
                return True
        return False

class theWall(Sprite):
    def __init__(self, model, w, h, x, y):
        super().__init__(model, w, h, x, y)

#------------------------------------------------------------

wallList = []

w1 = theWall('theWall.jpg', 600, 18, 330, 387)
w2 = theWall('theWall.jpg', 570, 18, 330, 506)
w3 = theWall('theWall.jpg', 570, 17, 330, 580)
w4 = theWall('theWall.jpg', 590, 18, 330, 700)
w5 = theWall('theWall.jpg', 970, 19, 330, 777)
w6 = theWall('theWall.jpg', 1030, 19, 300, 895)
w7 = theWall('theWall.jpg', 22, 490, 1473, 300)
w8 = theWall('theWall.jpg', 33, 487, 1300, 300)
w9 = theWall('theWall.jpg', 37, 100, 900, 500)
w10 = theWall('theWall.jpg', 40, 100, 290, 310)
w11 = theWall('theWall.jpg', 40, 100, 290, 699)

wallList.append(w1)
wallList.append(w2)
wallList.append(w3)
wallList.append(w4)
wallList.append(w5)
wallList.append(w6)
wallList.append(w7)
wallList.append(w8)
wallList.append(w9)
wallList.append(w10)
wallList.append(w11)

#---------------------------------------------------------------------------------------

myPlayer = Player('car_pygame2-removebg-preview.png', 70, 37, 0, 0, 5)

#---------------------------------------

enemy = Enemy('police_for_pygame-removebg-preview.png', 77, 45, 400, 300, 0)

#---------------------------------------

coin = Coin('coins-removebg-preview.png', 34.25, 28.4375, 100, 100)
coin.draw()
coinList.append(coin)

coin1 = Coin('coins-removebg-preview.png', 34.25, 28.4375, 150, 150)
coinList.append(coin1)
coin1.draw()

coin2 = Coin('coins-removebg-preview.png', 34.25, 28.4375, 200, 200)
coinList.append(coin2)
coin2.draw()

coin3 = Coin('coins-removebg-preview.png', 34.25, 28.4375, 250, 250)
coin3.draw()
coinList.append(coin3)

coin4 = Coin('coins-removebg-preview.png', 34.25, 28.4375, 300, 300)
coin4.draw()
coinList.append(coin4)

coin5 = Coin('coins-removebg-preview.png', 34.25, 28.4375, 350, 350)
coin5.draw()
coinList.append(coin5)

#---------------------------------------------------------------------------------------



for i in range(ENEMY_COUNT):
    newEnemy = Enemy('police_for_pygame-removebg-preview.png', 77, 45, randint(0, W), randint(0, H), 3)
    randomEnemies.append(newEnemy)



#---------------------------------------------------------------------------------------


isWin = True

#---

isGame = True

#---

run = True


while run:
    display.update()

    for e in event.get():
        if e.type == QUIT:
            run = False

    if isGame == True:
        myPlayer.move()
        if myPlayer.checkCollison() == True:
            isGame = False
            isWin = False

        enemy.chase(myPlayer)
        for e in randomEnemies:
            e.move()
    #--------------------------------------------------

        window.fill((0, 0, 0))
        window.blit(backgroud, (0, 0))
        myPlayer.draw()
        for wall in wallList:
            wall.draw()
        enemy.draw()
        for e in randomEnemies:
            e.draw()
    else:
        window.blit(game_over, (0, 0))

    timer.tick(FPS)