#This code is licensed under GPLv3; please see readme
#or code-license for more info

import sys,os
import pygame
from pygame.locals import *
import random

#Some base inits
version = "0.01"
debugmode = 0

#Let's get straight to business
pygame.init()
pygame.mixer.init()

fpsClock = pygame.time.Clock()

#resource loading functions
#loadimage - loads an image file with string name from /gfx
def loadimage(name):
    try:
        loadedimage = os.path.join("gfx", name)
    except pygame.error:
        print "Cannot load " + name + "!"
        pygame.quit()
        sys.exit()
    image = pygame.image.load(loadedimage)
    image = image.convert_alpha()
    return image

#loads a font in the root directory
def loadfont(name, size):
    try:
        loadedfont = os.path.join(name)
    except pygame.error:
        print "Cannot load font " + name + "!"
        pygame.quit()
        sys.exit()
    font = pygame.font.Font(loadedfont, size)
    return font

#loads sounds from /sfx
def loadsound(name):
    try:
        loadedsound = os.path.join("sfx", name)
    except pygame.error:
        print "Cannot load sound " + name + "!"
        pygame.quit()
        sys.exit()
    sound = pygame.mixer.Sound(loadedsound)
    return sound

def loadmusic(name):
    try:
        loadedmusic = os.path.join("music", name)
    except pygame.error:
        print "Cannot load music " + name + "!"
        pygame.quit()
        sys.exit()
    music = pygame.mixer.music.load(loadedmusic)
    return music

#set the display mode, caption and icon
pygame.display.set_mode((1024,768))
screen = pygame.display.get_surface()
pygame.display.set_caption("SCANDIVANIA: ALPHA NEON EX")

#load preliminary resources
mainfont = loadfont("stopmotion.ttf", 12)
logofont = loadfont("stopmotion.ttf", 30)

#htor
htor_attack = loadsound("htor/attack.wav")
htor_hurt = loadsound("htor/hurt.wav")
htor_taunt = loadsound("htor/taunt.wav")
htor_super = loadsound("htor/super.wav")
htor_ubertheme = loadsound("htor_superload.wav")
htor_death = loadsound("htor/death.wav")
htor_block = loadsound("htor/evade.wav")
htor_beep = loadsound("beep1.wav")

#vaenamoenen
vaen_attack = loadsound("vaenamoenen/attack.wav")
vaen_hurt = loadsound("vaenamoenen/hurt.wav")
vaen_taunt = loadsound("vaenamoenen/taunt.wav")
vaen_super = loadsound("vaenamoenen/super.wav")
vaen_ubertheme = loadsound("vaen_superload.wav")
vaen_death = loadsound("vaenamoenen/death.wav")
vaen_block = loadsound("vaenamoenen/evade.wav")
vaen_beep = loadsound("beep2.wav")

#other sounds
fret = loadsound("fret.wav")

musictoggle = 1
currenttrack = 0

#animations loading functions
def load_player_anim(animname, directory):
    animname[0] = loadimage(directory + "1.png")
    animname[1] = loadimage(directory + "2.png")
    animname[2] = loadimage(directory + "3.png")
    animname[3] = loadimage(directory + "4.png")
    animname[4] = loadimage(directory + "5.png")

def load_fx_anim(animname, directory):
    animname[0] = loadimage(directory + "1.png")
    animname[1] = loadimage(directory + "2.png")
    animname[2] = loadimage(directory + "3.png")
    animname[3] = loadimage(directory + "4.png")
    animname[4] = loadimage(directory + "5.png")
    animname[5] = loadimage(directory + "6.png")
    animname[6] = loadimage(directory + "7.png")
    animname[7] = loadimage(directory + "8.png")
    animname[8] = loadimage(directory + "9.png")
    animname[9] = loadimage(directory + "10.png")
    

#function for creating text
def createtext(usefont,text,surfx,surfy):
        textobj = usefont.render(text,1,(255,0,80))
        screen.blit(textobj,(surfx,surfy))

winmusicplayed = 0

#music player function
def musicplayer():
    global musictoggle, currenttrack, winmusicplayed
    playing = pygame.mixer.music.get_busy()
    if player1.win == 0 and player2.win == 0:
        if playing == False:
            currenttrack = random.randint(0,1)
            if currenttrack == 0:
                loadmusic("a_heros_battle.ogg")
            if currenttrack == 1:
                loadmusic("viking_knight.ogg")
            pygame.mixer.music.play(0)
    elif player1.win == 1 and winmusicplayed == 0:
        winmusicplayed = 1
        pygame.mixer.music.stop()
        loadmusic("htor_win.ogg")
        player1.win = 2
        pygame.mixer.music.play(0)
    elif player2.win == 1 and winmusicplayed == 0:
        winmusicplayed = 1
        pygame.mixer.music.stop()
        loadmusic("vaen_win.ogg")
        player2.win = 2
        pygame.mixer.music.play(0)

#classes
#player
#notes: the tables are for loading animations
class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadimage("button.png")
        self.rect = self.image.get_rect()
        self.x = 150
        self.y = 250
        self.framenr = 0
        self.frametime = 7
        self.win = 0
        self.anim = 1 #1 idle, 2 attack, 3 evade, 4 super, 5 taunt, 6 death
        self.health = 100
        self.factor = 1
        self.action = 0
        self.idle = [0,1,2,3,4]
        self.attack = [0,1,2,3,4]
        self.evade = [0,1,2,3,4]
        self.super = [0,1,2,3,4]
        self.taunt = [0,1,2,3,4]
        self.death = loadimage("button.png")
    def update(self):
        if self.health > 0 and self.win == 0:
            self.frametime -= 1
            if self.frametime <= 0:
                self.framenr += 1
                self.frametime = 7
            if self.framenr > 4:
                if self.anim <> 1 and self.win == 0:
                    self.anim = 1
                self.framenr = 0
            if self.anim == 1:
                screen.blit(self.idle[self.framenr], (self.x, self.y))
            if self.anim == 2:
                screen.blit(self.attack[self.framenr], (self.x, self.y))
            if self.anim == 3:
                screen.blit(self.evade[self.framenr], (self.x, self.y))
            if self.anim == 4:
                screen.blit(self.super[self.framenr], (self.x, self.y))
            if self.anim == 5:
                screen.blit(self.taunt[self.framenr], (self.x, self.y))
        elif self.health > 0 and self.win == 1:
            self.frametime -= 1
            if self.frametime <= 0:
                self.framenr += 1
                self.frametime = 4
            if self.framenr > 4:
                self.framenr = 0
            screen.blit(self.taunt[self.framenr], (self.x, self.y))
        elif self.health <= 0:
            self.frametime -= 1
            if self.frametime <= 0 and self.framenr < 6:
                self.framenr += 1
                self.frametime = 7
            screen.blit(self.death, (self.x, 430))

#effects (explosions etc)
class effect(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 10
        self.y = 280
        self.frame = 9
        self.anim = [0,1,2,3,4,5,6,7,8,9]
        self.frametime = 5
    def update(self):
        self.frametime -= 1
        if self.frametime < 0 and self.frame < 9:
            self.frametime = 5
            self.frame += 1
        if self.frame < 8:
            screen.blit(self.anim[self.frame], (self.x, self.y))

plr1explo = effect()
plr2explo = effect()
load_fx_anim(plr1explo.anim, "explosion/")
load_fx_anim(plr2explo.anim, "explosion/")
plr1lightning = effect()
plr2lightning = effect()
load_fx_anim(plr1lightning.anim, "lightning/")
load_fx_anim(plr2lightning.anim, "lightning/")
plr1btnxpl = effect()
plr2btnxpl = effect()
load_fx_anim(plr1btnxpl.anim, "xplosbtn/")
load_fx_anim(plr2btnxpl.anim, "xplosbtn/")
plr1btnxpl.y = 580
plr2btnxpl.y = 580

plr1explo.x = 350
plr2explo.x = 550
plr1lightning.x = 320
plr1lightning.y = 240
plr2lightning.x = 560
plr2lightning.y = 240
            
#create player instances
player1 = player()
player2 = player()

player1.x = 350
player2.x = 550

player1.death = loadimage("htor/death.png")
player2.death = loadimage("vaenamoenen/death.png")

#load anims
#player 1
load_player_anim(player1.idle, "htor/idle/")
load_player_anim(player1.attack, "htor/attack/")
load_player_anim(player1.evade, "htor/block/")
load_player_anim(player1.super, "htor/supa/")
load_player_anim(player1.taunt, "htor/taunt/")

#player 2
load_player_anim(player2.idle, "vaenamoenen/idle/")
load_player_anim(player2.attack, "vaenamoenen/attack/")
load_player_anim(player2.evade, "vaenamoenen/block/")
load_player_anim(player2.super, "vaenamoenen/supa/")
load_player_anim(player2.taunt, "vaenamoenen/taunt/")

#button arrays for holding/updating button objects
plr1buttons = []
plr2buttons = []
plr1successes = 0
plr2successes = 0

ytop = 565
ysize = 45

#game vars
plr1speed = 8
plr2speed = 8

allsprites = pygame.sprite.RenderUpdates()

plr1input = pygame.event.get(KEYDOWN)
plr2input = pygame.event.get(KEYDOWN)

#buttons
#LOTS OF EM you were warned
class button1(pygame.Rect):
    global plr1speed, plr1input, plr1successes, plr1btnxpl
    def __init__(self):
        self.keyname = "none"
        self.x = 20
        self.y = -40
        self.bx = 24
        self.by = 24
        self.image = loadimage("button.png")
        self.button = loadimage("button.png")
        self.fail = loadimage("failbtn.png")
        self.success = loadimage("succbtn.png")
        self.successful = 0
        self.rect = self.image.get_rect()
        self.speed = 2
        self.comingdown = 0
    def update(self):
        global plr1successes
        if self.comingdown == 1:
            self.y = self.y + plr1speed
        if event.type == KEYDOWN and self.successful == 0:
            if event.key == K_a:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "a" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "a" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
            if event.key == K_s:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "s" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "s" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
            if event.key == K_d:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "d" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop - 20 and self.keyname == "d" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
            if event.key == K_q:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "q" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "q" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
            if event.key == K_w:
                if self.y +(self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "w" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "w" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
            if event.key == K_e:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "e" and self.successful == 0:
                    self.successful = 1
                    plr1successes += 1
                    plr1btnxpl.x = self.x
                    plr1btnxpl.frame = 0
                    htor_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "e" and self.successful == 0:
                    self.successful = -1
                    plr1successes -= 1
                    fret.play()
        if self.y + (self.by/2) > ytop + ysize:
            if self.successful == 0:
                self.image = self.fail
            if self.successful == 1:
                self.image = self.success
        elif self.y + (self.by/2) < ytop + ysize and self.successful == 0:
            self.image = self.button
        elif self.y + (self.by/2) < ytop + ysize and self.successful == -1:
            self.image = self.fail
        elif self.y > 800:
            self.comingdown = 0
            self.y = -40
            self.successful = 0

class button2(pygame.Rect):
    global plr1speed, plr2input
    def __init__(self):
        self.keyname = "none"
        self.x = 20
        self.y = -40
        self.bx = 24
        self.by = 24
        self.image = loadimage("button.png")
        self.button = loadimage("button.png")
        self.fail = loadimage("failbtn.png")
        self.success = loadimage("succbtn.png")
        self.successful = 0
        self.rect = self.image.get_rect()
        self.speed = 2
        self.comingdown = 0
    def update(self):
        global plr2successes, plr2btnxpl
        if self.comingdown == 1:
            self.y = self.y + plr2speed
        if event.type == KEYDOWN:
            if event.key == K_j:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "j" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "j" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
            if event.key == K_k:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "k" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "k" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
            if event.key == K_l:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "l" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "l" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
            if event.key == K_u:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "u" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "u" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
            if event.key == K_i:
                if self.y +(self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "i" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "i" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
            if event.key == K_o:
                if self.y + (self.by/2) > ytop - 20 and self.y + (self.by/2) < ytop + ysize and self.keyname == "o" and self.successful == 0:
                    self.successful = 1
                    plr2successes += 1
                    plr2btnxpl.x = self.x
                    plr2btnxpl.frame = 0
                    vaen_beep.play()
                elif self.y + (self.by/2) < ytop and self.keyname == "o" and self.successful == 0:
                    self.successful = -1
                    plr2successes -= 1
                    fret.play()
        if self.y + (self.by/2) > ytop + ysize:
            if self.successful == 0:
                self.image = self.fail
            elif self.successful == 1:
                self.image = self.success
        elif self.y + (self.by/2) < ytop + ysize:
            self.image = self.button
        elif self.y > 800:
            self.comingdown = 0
            self.y = -40
            self.successful = 0

notesthisround = 15
prevroundnotes = notesthisround
noteincrement = 5
cur_round = 1
note_delay = 300
note_delay_2 = 300
round_delay = 300

#player 1
a = button1()
a.x = 30
a.keyname = "a"
s = button1()
s.x = 70
s.keyname = "s"
d = button1()
d.x = 110
d.keyname = "d"
q = button1()
q.x = 150
q.keyname = "q"
w = button1()
w.x = 190
w.keyname = "w"
e = button1()
e.x = 230
e.keyname = "e"

#player 2
j = button2()
j.x = 780
j.keyname = "j"
k = button2()
k.x = 820
k.keyname = "k"
l = button2()
l.x = 860
l.keyname = "l"
u = button2()
u.x = 900
u.keyname = "u"
i = button2()
i.x = 940
i.keyname = "i"
o = button2()
o.x = 980
o.keyname = "o"

betweenbursts = 100

plr1order = [1,2,3,4,5,6]
plr2order = [1,2,3,4,5,6]
plr1force = 0
plr2force = 0

delay = 100

difference = 0

plr2note = random.randint(1,6)
plr1note = random.randint(1,6)

#count if a number exists in the arrays
def countnumbers1():
    global plr1order
    if plr1order.count(1):
        a.comingdown = 1
        a.successful = 0
        a.y = -40
        plr1order[0] = 0
    elif plr1order.count(2):
        s.comingdown = 1
        s.successful = 0
        s.y = -40
        plr1order[1] = 0
    elif plr1order.count(3):
        d.comingdown = 1
        d.successful = 0
        d.y = -40
        plr1order[2] = 0
    elif plr1order.count(4):
        q.comingdown = 1
        q.successful = 0
        q.y = -40
        plr1order[3] = 0
    elif plr1order.count(5):
        w.comingdown = 1
        w.successful = 0
        w.y = -40
        plr1order[4] = 0
    elif plr1order.count(6):
        e.comingdown = 1
        e.successful = 0
        e.y = -40
        plr1order[5] = 0

def countnumbers2():
    global plr2order
    if plr2order.count(1):
        j.comingdown = 1
        j.successful = 0
        j.y = -40
        plr2order[0] = 0
    elif plr2order.count(2):
        k.comingdown = 1
        k.successful = 0
        k.y = -40
        plr2order[1] = 0
    elif plr2order.count(3):
        l.comingdown = 1
        l.successful = 0
        l.y = -40
        plr2order[2] = 0
    elif plr2order.count(4):
        u.comingdown = 1
        u.successful = 0
        u.y = -40
        plr2order[3] = 0
    elif plr2order.count(5):
        i.comingdown = 1
        i.successful = 0
        i.y = -40
        plr2order[4] = 0
    elif plr2order.count(6):
        o.comingdown = 1
        o.successful = 0
        o.y = -40
        plr2order[5] = 0


#randomizes notes
def generatenotes():
    global notesthisround, plr1speed, plr2speed, prevroundnotes, noteincrement, cur_round, note_delay, note_delay_2, betweenbursts, difference, plr1note, plr2note, plr1order, plr2order, plr1successes, plr2successes, player1, player2, delay
    note_delay -= plr1speed
    note_delay_2 -= plr2speed
    if note_delay <= 0 and plr1order <> [0,0,0,0,0,0] and betweenbursts <= 0:
        if plr1note == 1 and plr1order.count(1) > 0:
            a.comingdown = 1
            a.successful = 0
            a.y = -40
            plr1order[0] = 0
        elif plr1note == 1 and plr1order.count(1) == 0:
            countnumbers1()
        elif plr1note == 2 and plr1order.count(2) > 0:
            s.comingdown = 1
            s.successful = 0
            s.y = -40
            plr1order[1] = 0
        elif plr1note == 2 and plr1order.count(2) == 0:
            countnumbers1()
        elif plr1note == 3 and plr1order.count(3) > 0:
            d.comingdown = 1
            d.successful = 0
            d.y = -40
            plr1order[2] = 0
        elif plr1note == 3 and plr1order.count(3) == 0:
            countnumbers1()
        elif plr1note == 4 and plr1order.count(4) > 0:
            q.comingdown = 1
            q.successful = 0
            q.y = -40
            plr1order[3] = 0
        elif plr1note == 4 and plr1order.count(4) == 0:
            countnumbers1()
        elif plr1note == 5 and plr1order.count(5) > 0:
            w.comingdown = 1
            w.successful = 0
            w.y = -40
            plr1order[4] = 0
        elif plr1note == 5 and plr1order.count(5) == 0:
            countnumbers1()
        elif plr1note == 6 and plr1order.count(6) > 0:
            e.comingdown = 1
            e.successful = 0
            e.y = -40
            plr1order[5] = 0
        elif plr1note == 5 and plr1order.count(6) == 0:
            countnumbers1()
        note_delay = 150
    if note_delay_2 <= 0 and plr2order <> [0,0,0,0,0,0] and betweenbursts <= 0:
        if plr2note == 1 and plr2order.count(1) > 0:
            j.comingdown = 1
            j.successful = 0
            j.y = -40
            plr2order[0] = 0
        elif plr2note == 1 and plr2order.count(1) == 0:
            countnumbers2()
        elif plr2note == 2 and plr2order.count(2) > 0:
            k.comingdown = 1
            k.y = -40
            k.successful = 0
            plr2order[1] = 0
        elif plr2note == 2 and plr2order.count(2) == 0:
            countnumbers2()
        elif plr2note == 3 and plr2order.count(3) > 0:
            l.comingdown = 1
            l.y = -40
            l.successful = 0
            plr2order[2] = 0
        elif plr2note == 3 and plr2order.count(3) == 0:
            countnumbers2()
        elif plr2note == 4 and plr2order.count(4) > 0:
            u.comingdown = 1
            u.y = -40
            u.successful = 0
            plr2order[3] = 0
        elif plr2note == 4 and plr2order.count(4) == 0:
            countnumbers2()
        elif plr2note == 5 and plr2order.count(5) > 0:
            i.comingdown = 1
            i.y = -40
            i.successful = 0
            plr2order[4] = 0
        elif plr2note == 5 and plr2order.count(5) == 0:
            countnumbers2()
        elif plr2note == 6 and plr2order.count(6) > 0:
            o.comingdown = 1
            o.y = -40
            o.successful = 0
            plr2order[5] = 0
        elif plr2note == 6 and plr2order.count(6) == 0:
            countnumbers2()
        note_delay_2 = 150
    if plr2order == [0,0,0,0,0,0] and plr1order == [0,0,0,0,0,0]:
        delay -= 1
        if delay <= 0:
            cur_round += 1
            if betweenbursts > 15:
                betweenbursts = 100 - (3 * cur_round)
            elif betweenbursts <= 15:
                betweenbursts = 15
            difference = plr1successes - plr2successes #minus is Vaenamoenen's benefit
            if difference > 0:
                if difference > 0 and difference <= 2:
                    player2.factor = 1
                    player2.health -= (2 * player1.factor)
                    player1.factor += 1
                    player1.anim = 2
                    player1.framenr = 0
                    player2.anim = 3
                    player2.framenr = 0
                    plr2explo.frame = 0
                    htor_attack.play()
                    vaen_block.play()
                elif difference > 2 and difference <= 4:
                    player2.factor = 1
                    player2.health -= (5 * player1.factor)
                    player1.factor += 1
                    player1.anim = 2
                    player2.anim = 3
                    plr2explo.frame = 0
                    player1.framenr = 0
                    player2.framenr = 0
                    htor_attack.play()
                    vaen_block.play()
                elif difference >= 5:
                    player2.health -= (75 * player1.factor)
                    player1.anim = 4
                    player1.framenr = 0
                    player2.anim = 3
                    player2.framenr = 0
                    plr2lightning.frame = 0
                    htor_super.play()
                    htor_ubertheme.play()
                    vaen_block.play()
            elif difference < 0:
                if difference < 0 and difference >= -2:
                    player1.factor = 1
                    player1.health -= (2 * player2.factor)
                    player2.factor += 1
                    player2.framenr = 0
                    player2.anim = 2
                    player1.anim = 3
                    plr1explo.frame = 0
                    player1.framenr = 0
                    vaen_attack.play()
                    htor_block.play()
                    player2.framenr = 0
                elif difference < -2 and difference >= -4:
                    player1.factor = 1
                    player1.health -= (5 * player2.factor)
                    player1.anim = 3
                    player1.framenr = 0
                    player2.factor += 1
                    player2.anim = 2
                    player2.framenr = 0
                    plr1explo.frame = 0
                    vaen_attack.play()
                    htor_block.play()
                elif difference <= -5:
                    player1.health -= (75 * player2.factor)
                    player1.framenr = 0
                    player1.anim = 3
                    player2.anim = 4
                    player2.framenr = 0
                    plr1lightning.frame = 0
                    vaen_ubertheme.play()
                    vaen_super.play()
            elif difference == 0:
                player1.factor = 1
                player2.factor = 1
                player1.framenr = 0
                player2.framenr = 0
                player1.anim = 5
                player2.anim = 5
            plr1order = [1,2,3,4,5,6]
            if plr1speed < 16:
                plr1speed = plr1speed + 1
            plr1successes = 0
            plr2order = [1,2,3,4,5,6]
            if plr2speed < 16:
                plr2speed = plr2speed + 1
            plr2successes = 0
            difference = 0
            delay = 100 - (3 * cur_round)

#difference table
#0 = TAUNT
#1-2 = WEAK PUNCH (for winner)
#3-4 = PUNCH (for winner)
#5-6 = HYPER MEGA SUPER

#ggame update
def updategame():
    global plr1speed, plr2speed
    #player 1
    a.update()
    s.update()
    d.update()
    q.update()
    w.update()
    e.update()
    #player 2
    j.update()
    k.update()
    l.update()
    u.update()
    i.update()
    o.update()

def drawAll():
    #player 1
    screen.blit(a.image, (a.x, a.y))
    screen.blit(s.image, (s.x, s.y))
    screen.blit(d.image, (d.x, d.y))
    screen.blit(q.image, (q.x, q.y))
    screen.blit(w.image, (w.x, w.y))
    screen.blit(e.image, (e.x, e.y))
    createtext(mainfont, "j", 783,ytop+ysize+10)
    createtext(mainfont, "k", 823,ytop+ysize+10)
    createtext(mainfont, "l", 863,ytop+ysize+10)
    createtext(mainfont, "u", 903,ytop+ysize+10)
    createtext(mainfont, "i", 943,ytop+ysize+10)
    createtext(mainfont, "o", 983,ytop+ysize+10)
    #player 2
    screen.blit(j.image, (j.x, j.y))
    screen.blit(k.image, (k.x, k.y))
    screen.blit(l.image, (l.x, l.y))
    screen.blit(u.image, (u.x, u.y))
    screen.blit(i.image, (i.x, i.y))
    screen.blit(o.image, (o.x, o.y))
    createtext(mainfont, "a", 33,ytop+ysize+10)
    createtext(mainfont, "s", 73,ytop+ysize+10)
    createtext(mainfont, "d", 113,ytop+ysize+10)
    createtext(mainfont, "q", 153,ytop+ysize+10)
    createtext(mainfont, "w", 193,ytop+ysize+10)
    createtext(mainfont, "e", 233,ytop+ysize+10)

#a function VERY central to the game - updates all functional vars

bg = loadimage("negative.jpg")

mainmenu = 1
ending = 1

keepgamin = 1
gameon = 1

while keepgamin == 1:
    while mainmenu == 1:
        
        screen.fill(Color(255,255,255))
        
        createtext(logofont, "Type FIGHT to play", 300,350)
        createtext(mainfont, "Htor controls:", 100, 200)
        createtext(mainfont, "Q,W,E", 80,260)
        createtext(mainfont, "A,S,D", 80,280)
        createtext(mainfont, "Vanaemoenen controls:",800,200)
        createtext(mainfont, "U,I,O", 800,260)
        createtext(mainfont, "J,K,L", 800,280)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgamin = 0
                gameon = 0
                mainmenu = 0
            if event.type == KEYDOWN:
                mainmenu = 0
                gameon = 1

        pygame.display.flip()
        fpsClock.tick(50)
    
    while gameon == 1:

        plr1status = str(plr1successes)
        plr2status = str(plr2successes)
        plr1factor = str(player1.factor)
        plr2factor = str(player2.factor)

        screen.blit(bg, (0,0))

        plr2note = random.randint(1,6)
        plr1note = random.randint(1,6)

        if betweenbursts <= 0 and player1.health > 0 and player2.health > 0:
            generatenotes()

        if notesthisround <= 0:
            round_delay -= 1
        
        if round_delay <= 0:
            prevroundnotes = prevroundnotes + noteincrement
            notesthisround = prevroundnotes
            round_delay = 300
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameon = 0
                keepgamin = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameon = 0
                    mainmenu = 1
                if event.key == K_SPACE and player1.health < 0 or player2.health < 0:
                    gameon = 0

        #draw hit areas
        pygame.draw.rect(screen, Color(255,0,0), (20,ytop,260,ysize), 5)
        pygame.draw.rect(screen, Color(0,0,255), (760,ytop,260,ysize), 5)

        #draw HP bars
        pygame.draw.rect(screen, Color(0,255,0), (20,ytop-20,player1.health*1.5,10))
        pygame.draw.rect(screen, Color(0,255,0), (755,ytop-20,player2.health*1.5,10))

        #infotexts
        createtext(logofont, plr1factor, 200,ytop+ysize+40)
        createtext(logofont, plr2factor, 800,ytop+ysize+40)

        musicplayer()

        if betweenbursts > 0:
            betweenbursts -= 1
        
        updategame()

        #draw player 1
        player1.update()
        plr1explo.update()
        #draw player 2
        player2.update()
        plr2explo.update()
        #draw super effects
        plr1lightning.update()
        plr2lightning.update()
        drawAll()

        #only finally draw success explosions
        plr1btnxpl.update()
        plr2btnxpl.update()

        if player1.health <= 0:
            player2.win = 1
            createtext(logofont, "VAENAMOENEN CONQUERS", 300, 300)
        elif player2.health <= 0:
            player1.win = 1
            createtext(logofont, "THOR CONQUERS", 300, 300)
  
        pygame.display.flip()
        fpsClock.tick(50)

    

    pygame.quit()
    sys.exit()
