x = 2500
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *
import random
import math
window_width = 900
window_height = 700
window = display.set_mode( (window_width, window_height) )

bg = transform.scale( image.load("background.jpg"), (window_width, window_height) )
class Character():
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.image = transform.scale( image.load(self.filename), (self.size_x, self.size_y) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Wall(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = Surface( (size_x, size_y) )
        self.image.fill( (245, 49, 95) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

player1 = Character("cyborg.png", 50, 50, 30, 30, 8)
player2 = Character("hero.png", 50, 50, 300, 300, 5)
treasure = Character("treasure.png", 75, 75, 800, 600, 0)

# w1 = Wall(50, 300, 100, 100)
# w2 = Wall(50, 150, 300, 100)
# w3 = Wall(50, 300, 500, 100)
wall_list = []
wall_list.append( Wall(30, 300, 100, 100) )
wall_list.append( Wall(200, 30, 100, 400) )
wall_list.append( Wall(30, 150, 100, 550) )
wall_list.append( Wall(30, 550, 400, 0) )
wall_list.append( Wall(300, 30, 250, 550) )
wall_list.append( Wall(30, 500, 650, 200) )
wall_list.append( Wall(30, 100, 650, 0) )
wall_list.append( Wall(250, 30, 550, 300) )
wall_list.append( Wall(125, 30, 775, 500) )

# route_list = [(200, 300), (100, 500), (800, 100), (500, 700)]
route_list = []
for i in range(6):
    # Sol1
    # x = random.randint(0, window_width/5) * 5
    # y = random.randint(0, window_height/5) * 5
    x = random.randint(0, window_width)
    y = random.randint(0, window_height)
    route_list.append( (x, y) )
print(route_list)
route = 0
ok_x = False
ok_y = False

hp = 1

font.init()
style = font.SysFont(None, 50)

clock = time.Clock()
fps = 60

game = True
finish = False
while game:
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish == False:
        safety_x = player1.rect.x
        safety_y = player1.rect.y

        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and player1.rect.y > 0:
            player1.rect.y -= player1.speed
        elif keys_pressed[K_s] and player1.rect.y < window_height-player1.size_y:
            player1.rect.y += player1.speed
        elif keys_pressed[K_a] and player1.rect.x > 0:
            player1.rect.x -= player1.speed
        elif keys_pressed[K_d] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x += player1.speed

        for wall in wall_list:
            isCollide = sprite.collide_rect(player1, wall) 
            if isCollide:
                player1.rect.x = safety_x
                player1.rect.y = safety_y 

        goto_x, goto_y = route_list[route]
        if (ok_x == False):
            # Sol2
            d = abs(player2.rect.x - goto_x)
            if (player2.rect.x < goto_x):
                player2.rect.x += min(player2.speed, d)
            elif (player2.rect.x > goto_x):
                player2.rect.x -= min(player2.speed, d)
            else:
                ok_x = True
        if (ok_y == False):
            d = abs(player2.rect.y - goto_y)
            if (player2.rect.y < goto_y):
                player2.rect.y += min(player2.speed, d)
            elif (player2.rect.y > goto_y):
                player2.rect.y -= min(player2.speed, d) 
            else:
                ok_y = True
        
        if (ok_x == True and ok_y == True):
            route += 1
            ok_x = False
            ok_y = False
            if (route == len(route_list)):
                route = 0
            
        

        isCollide = sprite.collide_rect(player1, player2)
        if isCollide:
            hp -= 1
            player1.rect.x = 30
            player1.rect.y = 30
            if hp <= 0:
                print("YOU LOSE")
                finish = True
        isCollide = sprite.collide_rect(player1, treasure)
        if isCollide:
            print("YOU WIN")
            finish = True
    else: # finish == True
        if hp <= 0:
            text_result = style.render("YOU LOSE", True, (255, 255, 255))
        else:
            text_result = style.render("YOU WIN", True, (255, 255, 255))
        window.blit(text_result, (200, 200))

    text_hp = style.render("HP:"+str(hp), True, (255, 255, 255))
    window.blit(text_hp, (10, 10))

    player1.show()
    player2.show()
    treasure.show()

    for wall in wall_list:
        wall.show()

    display.update()
    clock.tick(fps)