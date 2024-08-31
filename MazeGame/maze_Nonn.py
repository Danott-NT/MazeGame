from pygame import *

window_width = 700
window_height =500
window = display.set_mode( (window_width, window_height) )

class Character(sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed):
        self.img = transform.scale(image.load(filename),(w,h))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw (self):
        window.blit(self.img,(self.rect.x,self.rect.y))

class Wall(Character):
    def __init__(self, x, y, w, h):
        self.img = Surface((w, h))
        self.img.fill((209, 27,27))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

bg = transform.scale(image.load("background.jpg"), (window_width, window_height))
player1 = Character("cyborg.png", 200, 300, 50, 50, 2)
player2 = Character("hero.png", 450, 430, 50, 50, 2)
player2_route = [(450, 200), (600, 200), (600, 450), (450, 450)]
player2_route_id = 0
target_x_ok = False
target_y_ok = False
player3 = Character("treasure.png", 620,430, 50, 50, 0)

wall_list = []
wall_list.append( Wall(250, 350, 25, 100))
wall_list.append( Wall(250, 350, 300, 25))
wall_list.append( Wall(150, 250, 300, 25))
wall_list.append( Wall(550, 100, 25, 300))
wall_list.append( Wall(300,100, 300, 25))
wall_list.append( Wall(100,100 , 200, 25))
    
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish ==  False:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and player1.rect.y > 0:
            player1.rect.y -= player1.speed
            for wall in wall_list:
                if ( sprite.collide_rect(player1, wall) ):
                    player1.rect.y += player1.speed
        if keys_pressed[K_s] and player1.rect.y < 420:
            player1.rect.y += player1.speed
            for wall in wall_list:
                if ( sprite.collide_rect(player1, wall) ):
                    player1.rect.y -= player1.speed
        if keys_pressed[K_d] and player1.rect.x < 615:
            player1.rect.x += player1.speed
            for wall in wall_list:
                if ( sprite.collide_rect(player1, wall) ):
                    player1.rect.x -= player1.speed
        if keys_pressed[K_a] and player1.rect.x > 0:
            player1.rect.x -= player1.speed 
            for wall in wall_list:
                if ( sprite.collide_rect(player1, wall) ):
                    player1.rect.x += player1.speed

    
            #if player2.rect.x > 625 or player2.rect.x < 8:
                #player2.speed *= -1

        #player2.rect.x += player2.speed

        target_x, target_y = player2_route[player2_route_id]
        if player2.rect.y != target_y:
            if player2.rect.y > target_y: #Go Up
                player2.rect.y -= player2.speed
            else:
                player2.rect.y += player2.speed
        else:
            target_y_ok = True

        if player2.rect.x != target_x:
            if player2.rect.x > target_x: #Go Up
                player2.rect.x -= player2.speed
            else:
                player2.rect.x += player2.speed
        
        else: 
            target_x_ok = True
        
        if target_x_ok and target_y_ok:
            print(player2_route_id, player2.rect.x, player2.rect.y)
            player2_route_id += 1
            if (player2_route_id >= len(player2_route)):
                player2_route_id = 0
            target_x_ok = False
            targer_y_ok = False

        window.blit(bg,(0,0))

        player1.draw()
        player2.draw()
        player3.draw()

        for wall in wall_list:
            wall.draw()

        if ( sprite.collide_rect(player1, player2)):
            print ("You Lose")
            finish = True
        if ( sprite.collide_rect(player1, player3)):
            print ("You Win")
            finish = True
    display.update()