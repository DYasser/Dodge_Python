#Code by Nabil Yasser // N.Y.
#King and Snakes Graphics from Bush -- http://blog-buch.rhcloud.com
#Swords Graphics from Joemaya & 'Tiilerdye' Frosted Fears Gaming
#Platforms Graphics from Kenney.nl
#Castle Background by blossomblairr
#Sounds Thanks to https://www.bfxr.net/
#Music background by "Kir"

import random, time
import pygame as pg
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

TITLE = "DODGE!"
WIDTH, HEIGHT = 1200, 600
FPS   = 60
HS_FILE = "highscore.txt"
font_name = pg.font.match_font('SH Pinscher')
# Player properties
P_width = 37
P_height = 60
PLAYER_GRAV = 0.8
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_JUMP = 14
#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)
BLUE  = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

PLATFORM_LIST = [(0,HEIGHT - 40, WIDTH, 40,"Plateform.png"),
                (0,HEIGHT/3,100,27,"Plateform (2).png"),
                (WIDTH-300,HEIGHT-180,100,20,"Plateform (2).png"),
                (300,HEIGHT-180,100,20,"Plateform (2).png"),
                (WIDTH-100,HEIGHT/3,100,27,"Plateform (2).png")]
ENNEMY_LIST = [()]
PORTAL_LIST = [(0,HEIGHT-200),(WIDTH-5,HEIGHT-200)]
#,(WIDTH/2+60,HEIGHT - 75)
MOB_LIST = [(0,HEIGHT - 75),(WIDTH-150,HEIGHT - 75)]
PLAT_MOVE_LIST = [(400,300,100,20,"Plateform (2).png")]
SWORDS = ["SWORD.png","sword1.png"]
vec = pg.math.Vector2

def draw_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_WIDTH  = 10
    fill = (pct /200) *BAR_LENGHT
    outline_rect = pg.Rect(x,y, BAR_LENGHT, BAR_WIDTH)
    fill_rect = pg.Rect(x,y,fill,BAR_WIDTH)
    pg.draw.rect(surf, WHITE, outline_rect, 3)
    pg.draw.rect(surf, GREEN, fill_rect)
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_right.png")).convert(),(P_width,P_height))
        self.image = Player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/2),(HEIGHT/2))
            #initial position of the player
        self.pos = vec(WIDTH/2,HEIGHT-50)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
            #what happens if the player press buttons
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_left.png")).convert(),(P_width,P_height))
            self.image = Player_img
            self.image.set_colorkey(WHITE)
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_right.png")).convert(),(P_width,P_height))
            self.image = Player_img
            self.image.set_colorkey(WHITE)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 *self.acc
            #Block the player and doesn't let him go out of the screen
        if self.rect.right >= WIDTH :
            self.pos.x = WIDTH-(P_width/2)-1
        elif self.rect.left <= 0:
            self.pos.x = (P_width/2)+1
        self.rect.midbottom  = self.pos
    def jump(self):
        if pg.sprite.spritecollide(self,self.game.platforms, False):
            self.vel.y += -PLAYER_JUMP
class Plateforms(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pg.sprite.Sprite.__init__(self)
        Plateform_img = pg.transform.scale(pg.image.load(path.join(img_dir, name)).convert(), (w,h))
        Plat_rect = Plateform_img.get_rect()
        self.image = pg.transform.scale(Plateform_img,(w,h))
        self.image.set_colorkey(BLACK)
        self.rect = Plat_rect
        self.rect.x = x
        self.rect.y = y
class Plateforms_Move(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pg.sprite.Sprite.__init__(self)
        Plateform_img = pg.transform.scale(pg.image.load(path.join(img_dir, name)).convert(), (w,h))
        Plat_rect = Plateform_img.get_rect()
        self.image = pg.transform.scale(Plateform_img,(w,h))
        self.image.set_colorkey(BLACK)
        self.rect = Plat_rect
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0,0)
        self.vel.x = 3
    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right >= WIDTH+1 or self.rect.left <= 0:
            self.vel = -self.vel
class Ennemies(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        Ennemies_img = pg.image.load(path.join(img_dir, random.choice(SWORDS))).convert()
        self.imageF = Ennemies_img
        self.imageF.set_colorkey(BLACK)
        self.image = self.imageF.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width  // 3
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-20,-10)
        self.speedy = random.randrange(3,16)
        self.speedx = random.randint(-1,1)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last = pg.time.get_ticks()
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last > 50:
            self.last = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pg.transform.rotate(self.imageF, self.rot)
            #Helps to manipulate the rotation and makes it look natural
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
class Mobs(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake.png")).convert(),(55,35))
        self.image = Mob_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width  -60
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
    def update(self):
        self.now = pg.time.get_ticks()
        self.rect.x += self.vel
            #Changes the direction if touches the limit of the map, and change image.
        if self.rect.right >= WIDTH+1 or self.rect.left <= 0:
            self.vel = -self.vel
            if self.vel < 0:
                Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake_re.png")).convert(),(55,35))
                self.image = Mob_img
                self.image.set_colorkey(WHITE)
                self.radius = self.rect.width  -60
            if self.vel > 0:
                Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake.png")).convert(),(55,35))
                self.image = Mob_img
                self.image.set_colorkey(WHITE)
                self.radius = self.rect.width  -60
class Portals(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Coins(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        Coin_img = pg.transform.scale(pg.image.load(path.join(img_dir, "coin0.png")).convert(),(20,20))
        self.image = Coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(21,WIDTH-21)
        self.rect.y = random.randrange(160,HEIGHT-80)
class Shields(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        Shield_img = pg.transform.scale(pg.image.load(path.join(img_dir, "Shield.png")).convert(),(20,15))
        self.image = Shield_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(21,WIDTH-21)
        self.rect.y = random.randrange(160,HEIGHT-80)
def print_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        pg.mixer.music.load(path.join(snd_dir, "All of 0 Hitpoints Left.ogg"))
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(loops=-1)
        self.load_data()
    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
    def new(self):
        # Defining all the variables and commands we need in the initialisation of a game
        self.running = True
        self.fullscreen = False
        self.rand = 0
        self.score = 0
        self.health = 200
        self.paused = False
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 150))
        self.start = pg.time.get_ticks()
                #Groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.ennemies = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.shields = pg.sprite.Group()
                #End of Groups
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for p in PORTAL_LIST:
            p = Portals(*p)
            self.all_sprites.add(p)
            self.portal.add(p)
        for i in range(3):
            ennemy = Ennemies()
            self.all_sprites.add(ennemy)
            self.ennemies.add(ennemy)
            if ennemy.rect.y > HEIGHT or ennemy.rect.x > WIDTH or ennemy.rect.x < 0:
                ennemy.kill()
                self.score += 10
        for p in PLATFORM_LIST:
            p = Plateforms(*p)
            self.platforms.add(p)
            self.all_sprites.add(p)
        for mob in MOB_LIST:
            mob = Mobs(*mob)
            self.all_sprites.add(mob)
            self.ennemies.add(mob)
        for p in PLAT_MOVE_LIST:
            p = Plateforms_Move(*p)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
    def run(self):
                # Game Loop, Every time the player re-plays
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    def update(self):
                    #Generates a coin
        self.now = pg.time.get_ticks()
        self.time = self.now - self.start
        if int(self.time) % 500 == 0:
            coin = Coins()
            self.coins.add(coin)
            self.all_sprites.add(coin)
                    #Generates a shield
        self.now = pg.time.get_ticks()
        self.time = self.now - self.start
        if int(self.time) % 900 == 0:
            shield = Shields()
            self.shields.add(shield)
            self.all_sprites.add(shield)
                # check if player hits a portal
        hits = pg.sprite.spritecollide(self.player,self.portal, False)
        for hit in hits:
            Portal_snd = pg.mixer.Sound(path.join(snd_dir,"Portal.wav"))
            Portal_snd.play()
            self.rand += 1
            if self.rand % 2 == 0:
                self.player.pos = (WIDTH- P_width, HEIGHT/4)
            if self.rand % 2 == 1:
                self.player.pos = (P_width+1, HEIGHT/4)
                    #If an ennemy goes off the screen
        for ennemy in self.ennemies:
            if ennemy.rect.left > WIDTH or ennemy.rect.right < 0:
                self.score += 10
                ennemy.kill()
                n = Ennemies()
                self.all_sprites.add(n)
                self.ennemies.add(n)
                    #Verifies if the player hits an ennemy
        hits = pg.sprite.spritecollide(self.player, self.ennemies,False, pg.sprite.collide_circle)
        for hit in hits:
            player_dmg_snd = pg.mixer.Sound(path.join(snd_dir, "Hit_Hurt3.wav"))
            player_dmg_snd.play()
            hit.kill()
            h = Ennemies()
            self.all_sprites.add(h)
            self.ennemies.add(h)
            self.player.image = pg.transform.scale(pg.image.load(path.join(img_dir, "king_hurt.png")).convert(),(P_width,P_height))
            self.player.image.set_colorkey(WHITE)
            hit = Mobs(random.randrange(60,WIDTH-60),HEIGHT - 75)
            self.all_sprites.add(hit)
            self.ennemies.add(hit)
            self.health -= 30
                #If the player got no more HPs: show game over screen!
            if self.health <= 0:
                g.show_go_screen()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                            #Verifies if an ennemy hits a platform: kill it.
        hits = pg.sprite.groupcollide(self.platforms,self.ennemies, False, True)
        for hit in hits:
            self.score += 5
            n = Ennemies()
            self.all_sprites.add(n)
            self.ennemies.add(n)
                            #Verifies if the player hit a coin
        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            Coin = pg.mixer.Sound(path.join(snd_dir, "Pickup_Coin.wav"))
            Coin.play()
            self.score += 100
                            #Verifies if the player hit a Shield
        hits = pg.sprite.spritecollide(self.player, self.shields, True)
        for hit in hits:
            Shield_snd = pg.mixer.Sound(path.join(snd_dir, "Pickup_Shield.wav"))
            Shield_snd.play()
            self.health += 20
            if self.health > 200:
                self.health = 200
                # Game Loop - Update
        self.all_sprites.update()
    def events(self):
        P_JUMP = pg.mixer.Sound(path.join(snd_dir,"Jump.wav"))
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    P_JUMP.play()
                    if self.paused == False:
                        self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_r:
                    self.show_start_screen()
                if event.key == pg.K_ESCAPE:
                    if self.fullscreen:
                        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
                        self.fullscreen = False
                    elif not self.fullscreen:
                        self.screen = pg.display.set_mode((WIDTH,HEIGHT),pg.FULLSCREEN)
                        self.fullscreen = True
    def draw(self):
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.now = pg.time.get_ticks()
        self.time = self.now - self.start
        # Game Loop - draw
        self.screen.blit(backG, backG_rect)
        self.all_sprites.draw(self.screen)
        print_text(self.screen, "Score: "+str(self.score), 22, WIDTH/2, 15)
        print_text(self.screen, "Time: "+str(int(self.time/1000))+"s",22, WIDTH/2,40)
        draw_health(self.screen, 10, 10, self.health)
        # *after* drawing everything, flip the display
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            print_text(self.screen,"Paused", 105, WIDTH / 2, HEIGHT / 2 - 50)
            print_text(self.screen,"Press P to unpause", 20, WIDTH / 2, HEIGHT / 2+30)
            print_text(self.screen,"Arrow Keys to move right and left", 25, WIDTH / 2, HEIGHT / 2+200)
            print_text(self.screen,"Space bar to jump", 25, WIDTH / 2, HEIGHT / 2 +230)
            print_text(self.screen,"Press R to reset the game", 25, WIDTH / 2, HEIGHT / 2 +170)
            print_text(self.screen,"Escape to toggle fullscreen", 25, WIDTH / 2, HEIGHT / 2 +260)
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background31.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        print_text(self.screen, "SpaceBAR: Jump",30, WIDTH-121, 100)
        print_text(self.screen, "ArrowKeys(L/R): Move",30, WIDTH-130, 44)
        print_text(self.screen, "P: pause the game",30, WIDTH-120, 72)
        print_text(self.screen, "R: reset the game",30, WIDTH-120, 96+32)
        print_text(self.screen, "Escape: un/fullscreen",30, WIDTH-120, 96+28+32)
        print_text(self.screen, "Stay alive the longest",32, 200, 80)
        print_text(self.screen, "period possible.",32, 200, 120)
        print_text(self.screen, "Dodge every attack and",32, 200, 160)
        print_text(self.screen, "collect coins to gain more points",32, 210, 200)
        print_text(self.screen, ", and crowns to heal up!",32, 200, 240)
        print_text(self.screen, "Every time an ennemy hits you",32, 210, 380)
        print_text(self.screen, "he respawns",32, 200, 420)
        print_text(self.screen, "and a different ennemy spawns!",32, 210, 460)
        print_text(self.screen, "Don't let them hit you!",32, 200, 500)
        print_text(self.screen, "DODGE!",80, WIDTH/2 +60, HEIGHT/4-100)
        print_text(self.screen, "Press a key to Start",30, WIDTH/2 + 60, HEIGHT*1.5/2)
        print_text(self.screen,"High Score: " + str(self.highscore), 22, WIDTH / 2+60, 15)
        pg.display.flip()
        time.sleep(0.25)
        self.Waiting()
    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        print_text(self.screen, "GAME OVER",200, WIDTH/2, 200)
        pg.display.flip()
        time.sleep(1)
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        print_text(self.screen, "DODGE!",80, WIDTH/2, HEIGHT/4-100)
        print_text(self.screen, "Press a Key to Restart",30, WIDTH/2, HEIGHT-100)
        if self.score > self.highscore:
            self.highscore = self.score
            print_text(self.screen,"NEW HIGH SCORE!",40, WIDTH / 2, HEIGHT / 2 + 40)
            print_text(self.screen,"Score: " + str(self.score), 40, WIDTH / 2, HEIGHT / 2 + 90)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            print_text(self.screen,"High Score: " + str(self.highscore),40, WIDTH / 2, HEIGHT / 2 + 40)
            print_text(self.screen,"Score: " + str(self.score), 40, WIDTH / 2, HEIGHT / 2 + 90)
        pg.display.flip()
        time.sleep(2)
        self.Waiting()
    def Waiting(self):
        waiting = True
        while waiting == True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYUP:
                    waiting = False
                    g.new()
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen
pg.quit()
