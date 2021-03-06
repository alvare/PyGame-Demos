#!/usr/bin/env python
import pygame
from pygame.locals import *
from random import randint, choice, shuffle
from math import cos, sin, pi, pow, fabs, trunc
try:
    import psyco
    psyco.full()
except ImportError:
	print "Psyco not found, install it faggot."
#Creation
timer = 0
try: #Reading options
    opt = open('options.txt','r')
    if int(opt.readline()[-2:-1]):
        fullscr = True
    else:
        fullscr = False
    players = int(opt.readline()[-1])
    print "Now playing "+str(players)+" players."
except:
    opt = open('options.txt','w')
    opt.write('fullscreen=0\nplayers=2')
    fullscr = False
    print "Creating option file."
opt.close()
if fullscr:
    scr = pygame.display.set_mode((1024,768),FULLSCREEN)
else:
    scr = pygame.display.set_mode((800,600))

pygame.mixer.init(44100,-16,2,1024)
w,h = scr.get_size()
WIN = -1
pygame.mouse.set_visible(False)
clk = pygame.time.Clock()
extratime = 0
background = [50,50,200]
megaloop = True
pygame.font.init()
ui_font = pygame.font.Font(None,36)
font = pygame.font.Font(None,30)
font2 = pygame.font.Font(None,128)
piso = pygame.image.load('./piso2.bmp')
piso.set_colorkey((255,255,255))
wins = [0 for x in range(players)] # Player N
class Cachoso:
    def __init__(self, scr):
        self.scr = scr
        self.x = randint(100, w)
        self.y = randint(0, 350)
        self.spd = 5
        self.img = pygame.surface.Surface((32,32))
        self.img.fill((200,0,0))
        self.angle = randint(0, trunc(2*pi))
        #self.derivate = 1
        self.xspd = 0
        self.yspd = 0
        self.direction = 1
        self.time = pygame.time.get_ticks()
        self.z = randint(0, trunc(2*pi))
    def magic(self):
        self.z += 0.005*pi
        return cos(self.z)*sin(2*self.z)*cos(self.z*1/10+pi)
    def update(self):
        #self.derivate += pow(-1,randint(1,2))*randint(1,5)/100
        #self.angle = self.derivate
        #if randint(-10,10) == 0 and (pygame.time.get_ticks()-self.time) > 1000: 
        #    self.direction *= -1
        #    self.time = pygame.time.get_ticks()
        a = self.magic()
        self.angle += a
        #print self.angle, self.xspd, self.yspd, a
        self.xspd = cos(self.angle)*self.spd
        self.yspd = sin(self.angle)*self.spd
        if (self.x < 0 and self.xspd <= 0) or (self.x+self.img.get_width() >= w and self.xspd > 0):
            self.angle = 180*pi/180 - self.angle
        if self.y < 0 and self.yspd <= 0:
            self.angle *= -1
        try:
            if self.scr.get_at((trunc(self.x+self.img.get_width()/2),trunc(self.y+1+self.img.get_height()))) != (background[0],background[1],background[2],255) and self.yspd > 0:
                self.angle *= -1
        except: pass
        """if self.x <= 0:
            self.xspd = fabs(self.xspd)
        elif self.x+self.img.get_width() >= w:
            self.xspd = fabs(self.xspd)*-1
        if self.y <= 0:
            self.yspd = fabs(self.yspd)
        try:
            if self.scr.get_at((trunc(self.x+self.img.get_width()/2),trunc(self.y+1+self.img.get_height()))) != (background[0],background[1],background[2],255):
                self.yspd = fabs(self.yspd)*-1
                print "----------------------"
        except: pass"""
        self.x += self.xspd
        self.y += self.yspd
        self.scr.blit(self.img, (self.x, self.y))
        return ((self.x,self.y),(self.img.get_width(),self.img.get_height()))
class Steve:
    def __init__(self, scr, img, kontrol, player):
        self.x = 1
        self.y = 1
        self.xspd = 0
        self.yspd = 0
        self.scr = scr
        self.img = pygame.image.load(img).convert()
        self.w,self.h = self.img.get_size()
        self.img.set_colorkey((255,255,255))
        self.falling = False
        self.left,self.right,self.up = kontrol
        self.plyr = player
    def update(self,rect, coso):
        global WIN
        key = pygame.key.get_pressed()
        #Horizontal movement
        if not (self.xspd > 10 or self.xspd < -10):
            if key[self.left]:
                self.xspd -= 2
            if key[self.right]:
                self.xspd += 2
        #Jump
        if key[self.up] and not self.falling:
            self.yspd = -20
        #Close to 0 control
        if -2 < self.xspd < 2:
            self.xspd = 0
        #Friction
        if self.xspd > 0:
            self.xspd -= 1
        elif self.xspd < 0:
            self.xspd += 1
        #Gravity
        self.yspd += 1 if self.falling else 0
        self.y += self.yspd
        self.x += self.xspd
        #Border handling
        if self.x+self.img.get_width()/2 < 0+2:
            self.x = 0-1*self.img.get_width()/2+2
        elif self.x+self.img.get_width()/2 > w-1:
            self.x = w-self.img.get_width()/2-2
        #Floor detection
        try:
            while self.scr.get_at((self.x+self.img.get_width()/2,self.y+self.img.get_height())) != (background[0],background[1],background[2],255):
                self.y -= 1
                self.falling = False
                self.yspd = 0
            if self.scr.get_at((self.x+self.img.get_width()/2,self.y+1+self.img.get_height())) != (background[0],background[1],background[2],255):
                self.falling = False
                self.yspd = 0
            else:
                self.falling = True
        except:
            self.falling = True
        #Collision ???
        loping = True
        for a in rect:
            if pygame.Rect((self.x,self.y,self.w,self.h)).collidepoint(a[0][0],a[0][1]) or pygame.Rect((self.x,self.y,self.w,self.h)).collidepoint(a[1][0],a[1][1]):
                loping = False
        if pygame.Rect((self.x,self.y,self.w,self.h)).colliderect(coso):
            WIN = self.plyr
        scr.blit(self.img,(self.x,self.y))
        return loping

class Raya:
    def __init__(self, scr, spd):
        self.img = pygame.image.load('raya.bmp')
        self.img.set_colorkey((255,255,255))
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = randint(-self.w,w)
        self.y = choice((-self.h,h+self.h))
        self.inverted = False
        if self.y > 0:
            self.inverted = True
            self.img = pygame.transform.flip(self.img,1,1)
        if self.y > h:
            self.spd = -spd
        else:
            self.spd = spd
        self.scr = scr
    def update(self):
        self.y += self.spd
        self.scr.blit(self.img,(self.x,self.y))
        if not self.inverted:
            return ((self.x+self.w/2,self.y),(self.x+self.w/2,self.y+self.h/2))
        else:
            return ((self.x+self.w/2,self.y+self.h),(self.x+self.w/2,self.y+self.h/2))
    def pos(self):
        return [self.x]+[self.y]+[self.img.size()]

def MenuItem(txt, bgcolor, N):
    ui_txt = ui_font.render(txt,1,(0,0,0),(bgcolor))
    ui_button = pygame.Surface((250,50))
    ui_button.fill((bgcolor))
    scr.blit(ui_button,(w/2-250/2,h/2-50/2-200+N*60))
    scr.blit(ui_txt,(w/2-250/2+(250-ui_txt.get_width())/2,h/2-50/2-200+N*60+(50-ui_txt.get_height())/2))

#MAIN main LUP
while megaloop:
    #Menu UI
    stv = []
    stv.append(Steve(scr,'1.bmp',(K_LEFT,K_RIGHT,K_UP),0))
    if players > 1:
        stv.append(Steve(scr,'2.bmp',(K_a,K_d,K_w),1))
    if players > 2:
        stv.append(Steve(scr,'3.bmp',(K_h,K_k,K_u),2))
    if players > 3:
        stv.append(Steve(scr,'4.bmp',(K_KP4,K_KP6,K_KP8),3))

    mantaraya = [Raya(scr,30),Raya(scr,30)]
    coso = Cachoso(scr)
    loop2 = True
    scr.fill((50,100,50))
    while loop2:
        MenuItem('1 - Play',(200,100,200),1)
        MenuItem('2 - HiScore',(100,250,50),2)
        MenuItem('3 - Fullscreen',(200,200,200),3)
        MenuItem('4 - Exit',(255,10,10),4)
        clk.tick(100)
        extratime += 0.01
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_1 or e.key == K_RETURN:
                    select = 1
                    loop2 = False
                elif e.key == K_2:
                    select = 2
                    loop2 = False
                elif e.key == K_3:
                    select = 3
                    loop2 = False
                elif e.key == K_ESCAPE or e.key == K_4:
                    megaloop = False
                    loop2 = False
                    select = 4

    if select == 1:
        #Some definitions
        maxrand = 10 #raya probabilty
        extratime += timer/1000
        loop = True
        pause = False
        alfa = True
        #Main LUP -------------------------------------------------------#
        if randint(1,50) > 2:
            pygame.mixer.music.load('music'+str(randint(1,9))+'.mp3')
        else:
            pygame.mixer.music.load('extra.mp3')
        #pygame.mixer.music.play(-1)
        while loop:
            scr.fill(background)
            #Piso
            scr.blit(piso,(0,h/2+h/6))
            #Random Raya generator
            if randint(0,int(maxrand)) ==  1:
                mantaraya += [Raya(scr,randint(10,20))]
            #Updating
            winrar = coso.update()
            rayas_rect = []
            for b in range(len(mantaraya)):
                rayas_rect.append(mantaraya[b].update())
            lista = range(len(stv))
            shuffle(lista)
            if alfa:
                for b in lista:
                    dada = stv[b].update(rayas_rect, winrar)
                    if not dada:
                        del stv[b]
                        break
                if len(stv) < 2:
                    wins[stv[0].plyr] += 1
                    loop = False
                    alfa = False
            if WIN != -1:
                loop = False
                wins[WIN] += 1
            #Destroying others
            for b in range(len(mantaraya)):
                if mantaraya[b].y > h+mantaraya[b].img.get_height()*2:
                    del mantaraya[b]
                    break
                elif mantaraya[b].y < -mantaraya[b].img.get_height()*2:
                    del mantaraya[b]
                    break
            #Timer
            for b in range(len(stv)):
                txt = font.render(str(wins[b]),1,(10,10,10))
                scr.blit(txt,(w/len(stv)*b+1,1))

            pygame.display.flip()
            #Pseudo keyboard handler
            for e in pygame.event.get():
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    loop = 0
                elif e.type == KEYDOWN and e.key == K_p:
                    pause = True
                else:
                    pause = False
            #Pause
            if pause:
                loop3 = True
                while loop3:
                    clk.tick(1)
                    extratime += 1
                    for e in pygame.event.get():
                        if e.type == KEYDOWN and e.key == K_p:
                            loop3 = False
                            pause = False
                            break
            clk.tick(30)
            #maxrand -= 0.005
            if int(maxrand) <= 0:
                maxrand = 1

        #Ending -----------------------------------------#
        extratime += 1
        srfc = pygame.Surface((w,h))
        srfc.fill((0,0,0))
        srfc.set_alpha(20)
        pygame.mixer.music.fadeout(1000)
        for b in range(60):
            clk.tick(60)
            scr.blit(srfc,(0,0))
            pygame.display.flip()
        scr.fill((0,0,0))
        print pygame.time.get_ticks()-extratime*1000
        if WIN == -1:
            txt = font2.render("Player "+str(stv[0].plyr+1)+" WINS",1,(randint(0,255),randint(0,255),randint(0,255)),(0,0,0))
        else:
            txt = font2.render("Player "+str(WIN+1)+" WINS",1,(randint(0,255),randint(0,255),randint(0,255)),(0,0,0))
            WIN = -1
        scr.blit(txt,(w/2-txt.get_width()/2,h/2-txt.get_height()/2))
        pygame.display.flip()
        a=True
        while a:
            for e in pygame.event.get():
                if e.type is KEYDOWN and e.key in [K_RETURN,K_ESCAPE, K_1]:
                    a = False
    elif select == 2:
        alls = []
        scores = open('hiscore.txt','r')
        alls = scores.readlines()
        maxim = int(alls.pop())
        for b in alls:
            if int(b) > maxim:
                maxim = int(b)
        scr.fill((150,20,230))
        print maxim
        txt = font2.render(str(maxim),1,(0,0,0))
        scr.blit(txt,(w/2-txt.get_width()/2,h/2-txt.get_height()/2))
        pygame.display.flip()
        a = True
        while a:
            extratime += 0.01
            clk.tick(100)
            for e in pygame.event.get():
                if e.type in [KEYDOWN,MOUSEBUTTONDOWN]:
                    a = False
    elif select == 3:
        opt = open('options.txt','w')
        if fullscr:
            opt.write('fullscreen=0\nplayers='+str(players))
        else:
            opt.write('fullscreen=1\nplayers='+str(players))
        opt.close()
        exit()
    timer = pygame.time.get_ticks()-extratime*1000
    del mantaraya
    del stv
scr.fill((255,255,255))
logo = pygame.image.load('pygame_powered.gif').convert()
scr.blit(logo,(w/2-logo.get_width()/2,h/2-logo.get_height()/2))
pygame.display.flip()
pygame.time.wait(100)
pygame.quit()
exit()
