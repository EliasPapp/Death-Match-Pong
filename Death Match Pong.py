# -*- coding: latin1 -*-
from pygame import *
from pygame.locals import *
import pygame
import time
import Box2D as b2
import linecache
from random import randint
pygame.init()
mixer.init()
pygame.font.init()
Gname = 'Deathmatch Pong'
screen = pygame.display.set_mode((1060, 600))
pygame.display.set_caption(Gname)
font = pygame.font.SysFont('trebuchet MS', 32)
font2 = pygame.font.SysFont('trebuchet MS', 45)
font3 = pygame.font.SysFont('trebuchet MS', 23)
FPS = 35
fpsClock = pygame.time.Clock()
world = b2.b2World((0, 0), True)

# PPM and colors
PPM = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHIP1 = (75, 202, 157)
SHIP2 = (224, 210, 53)
SHIP3 = (219, 52, 52)
SHIP4 = (95, 53, 221)

# Textures
TScreen = pygame.image.load('Textures/titlescreen.png')
Credits = pygame.image.load('Textures/credits.png')
credx = -900
credy = -900
Instructions = pygame.image.load('Textures/instructions.png')
instx = -900
insty = -900
Ctrls = pygame.image.load('Textures/ctrls.png')
Ctrls2 = pygame.image.load('Textures/ctrls2.png')
ctrlsx = 297
ctrlsy = 77
Quebec = pygame.image.load('./Textures/Fquebec.png')
Ontario = pygame.image.load('./Textures/Fontario.png')
Nunavut = pygame.image.load('./Textures/Fnunavut.png')
Floors = [Quebec, Ontario, Nunavut]
Vwall = pygame.image.load('Textures/twall.png')
S1 = pygame.image.load('Textures/ship1.png')
S2 = pygame.image.load('Textures/ship2.png')
S3 = pygame.image.load('Textures/ship3.png')
S4 = pygame.image.load('Textures/ship4.png')
S5 = pygame.image.load('Textures/ship5.png')
S6 = pygame.image.load('Textures/ship6.png')
S7 = pygame.image.load('Textures/ship7.png')
S8 = pygame.image.load('Textures/ship8.png')
Skin = [S1, S2, S3, S4, S5, S6, S7, S8]
TxtSkin = [SHIP1, SHIP2, SHIP3, SHIP4, SHIP1, SHIP2, SHIP3, SHIP4]
BA = pygame.image.load('Textures/ball.png')
Tpy = pygame.image.load('Textures/bronze.png')
S2 = pygame.transform.rotate(S2, 180)
S3 = pygame.transform.rotate(S3, -90)
S4 = pygame.transform.rotate(S4, 90)
Timer = False

# Unalterable text
Ver = font.render('Versão: 1.0', True, WHITE)
Pla = font2.render('Jogadores', True, WHITE)
Ins = font2.render('nstruções', True, WHITE)
Cre = font2.render('réditos', True, WHITE)

#Flags
c = 0
d = 1
e = 2
f = 3

# Left Side Wall
SwallW = 0.8
SwallH = 21.4
Swall = pygame.transform.rotate(Vwall, 90)
LWallDef = b2.b2BodyDef()
LWallDef.type = b2.b2_staticBody
Lwall = world.CreateBody(LWallDef)
LwallFixture = b2.b2FixtureDef()
LwallFixture.shape = b2.b2PolygonShape(box=(SwallW, SwallH))
LwallFixture.restitution = 0
Lwall.CreateFixture(LwallFixture)
# Right Side Wall
Rwall = world.CreateBody(LWallDef)
Rwall.CreateFixture(LwallFixture)
# Top Wall
TWallDef = b2.b2BodyDef()
TWallDef.position = (-100.0, -100.0)
TWallDef.type = b2.b2_staticBody
Twall = world.CreateBody(TWallDef)
TwallFixture = b2.b2FixtureDef()
TwallFixture.shape = b2.b2PolygonShape(box=(SwallH, SwallW))
TwallFixture.restitution = 0
Twall.CreateFixture(TwallFixture)
# Bottom Wall
Bwall = world.CreateBody(TWallDef)
Bwall.CreateFixture(TwallFixture)

# Bumpers
BumpPos = [(25, 2.1), (81, 2.1), (25, 58.1), (81, 58.1)]
BumpList = []
# Define bumpers
def create_bumper(bumper_def):
    bumper = world.CreateBody(bumper_def)
    bumperFixture = b2.b2FixtureDef()
    bumperFixture.friction = 0
    bumperFixture.restitution = 0
    bumperFixture.density = 1000000 * 1000000
    bumperFixture.shape = b2.b2CircleShape(radius=6.5)
    bumper.CreateFixture(bumperFixture)
    return bumper
# Bumper positions
for i in range(4):
    bodyDef = b2.b2BodyDef()
    bodyDef.position = BumpPos[i]
    bodyDef.type = b2.b2_dynamicBody
    bumper = create_bumper(bodyDef)
    BumpList.append(bumper)

# Player 1
IUP = 10
P1HP = IUP
P1Scr = 0
sSpd1 = 0
Xmov = 300 * 1000
Sdamp = 11
Ship1Def = b2.b2BodyDef()
Ship1Def.linearDamping = Sdamp
Ship1Def.position = (53, 58.1)
Ship1Def.type = b2.b2_dynamicBody
ship1 = world.CreateBody(Ship1Def)
shipFixture = b2.b2FixtureDef()
shipFixture.friction = 0
shipFixture.restitution = 4
shipFixture.density = 1000
shipFixture.shape = b2.b2CircleShape(radius=5)
ship1.CreateFixture(shipFixture)
# Define Player 1
def draw_ship(ship1):
    global ship1X, ship1Y, ship1Pos
    shape = ship1.fixtures[0].shape
    if shape.type == b2.b2Shape.e_circle:
        ship1Pos = ship1.position
        ship1X = int(ship1Pos[0] * PPM)
        ship1Y = int(ship1Pos[1] * PPM)
        screen.blit(S1, (ship1X-50, ship1Y-50))

# Player 2
P2HP = IUP
P2Scr = 0
sSpd2 = 0
Ship2Def = b2.b2BodyDef()
Ship2Def.linearDamping = Sdamp
Ship2Def.position = (53, 2.099)
Ship2Def.type = b2.b2_dynamicBody
ship2 = world.CreateBody(Ship2Def)
ship2.CreateFixture(shipFixture)
# Define Player 2
def draw_ship2(ship2):
    global ship2X, ship2Y, ship2Pos
    shape = ship2.fixtures[0].shape
    if shape.type == b2.b2Shape.e_circle:
        ship2Pos = ship2.position
        ship2X = int(ship2Pos[0] * PPM)
        ship2Y = int(ship2Pos[1] * PPM)
        screen.blit(S2, (ship2X-50, ship2Y-50))

# Player 3
P3HP = IUP
P3Scr = 0
sSpd3 = 0
Ship3Def = b2.b2BodyDef()
Ship3Def.linearDamping = Sdamp
Ship3Def.position = (25, 30)
Ship3Def.type = b2.b2_dynamicBody
ship3 = world.CreateBody(Ship3Def)
ship3.CreateFixture(shipFixture)
# Define Player 3
def draw_ship3(ship3):
    global ship3X, ship3Y, ship3Pos
    shape = ship3.fixtures[0].shape
    if shape.type == b2.b2Shape.e_circle:
        ship3Pos = ship3.position
        ship3X = int(ship3Pos[0] * PPM)
        ship3Y = int(ship3Pos[1] * PPM)
        screen.blit(S3, (ship3X-50, ship3Y-50))

# Player 4
P4HP = IUP
P4Scr = 0
sSpd4 = 0
Ship4Def = b2.b2BodyDef()
Ship4Def.linearDamping = Sdamp
Ship4Def.position = (81, 30)
Ship4Def.type = b2.b2_dynamicBody
ship4 = world.CreateBody(Ship4Def)
ship4.CreateFixture(shipFixture)
# Define Player 4
def draw_ship4(ship4):
    global ship4X, ship4Y, ship4Pos
    shape = ship4.fixtures[0].shape
    if shape.type == b2.b2Shape.e_circle:
        ship4Pos = ship4.position
        ship4X = int(ship4Pos[0] * PPM)
        ship4Y = int(ship4Pos[1] * PPM)
        screen.blit(S4, (ship4X-50, ship4Y-50))

# Ball
spdX = -0.9925
spdY = 1  # random.uniform(0, 10)
ballDef = b2.b2BodyDef()
ballDef.position = (53, 30)
ballDef.type = b2.b2_dynamicBody
ball = world.CreateBody(ballDef)
# Ball fixture
ballFixture = b2.b2FixtureDef()
ballFixture.friction = 0
ballFixture.restitution = 1
ballFixture.density = 0.000000001
ballFixture.shape = b2.b2CircleShape(radius=1.4)
ball.CreateFixture(ballFixture)

# Define ball
def draw_ball(ball):
    global ballX, ballY
    shape = ball.fixtures[0].shape
    if shape.type == b2.b2Shape.e_circle:
        ballPos = ball.position
        ballX = int(ballPos[0] * PPM)
        ballY = int(ballPos[1] * PPM)
        screen.blit(BA, (ballX-14, ballY-14))

# Define Box2D Rules
def calculate_rules():
    world.Step(1.0/30.0, 8, 5)
# Title screen
while True:
    IUP = 10
    P1Scr = P2Scr = P3Scr = P4Scr = 0
    z = randint(0, 2)
    Floor = Floors[z]
    TwoPlayers = False
    TitleScreen = True
    GameRunning = False
    GameEnded = False

    for i in range(255, 0, -12):
        screen.blit(TScreen, (0, 0))
        fade = pygame.Surface((1060, 600))
        fade.set_alpha(i)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)

    if not GameRunning:
        Menu = mixer.music.load('Sounds/menu.ogg')
        mixer.music.play(-1)
    while TitleScreen:
        screen.blit(TScreen, (0, 0))
        screen.blit(Ver, (885, 8))
        screen.blit(Pla, (470, 352))
        screen.blit(Pla, (470, 410))
        screen.blit(Ins, (450, 468))
        screen.blit(Cre, (450, 526))
        screen.blit(Credits, (credx, credy))
        screen.blit(Instructions, (instx, insty))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_c:
                    credx = 166
                    credy = 20
                if event.key == K_i:
                    instx = 166
                    insty = 20
            if event.type == KEYUP:
                if event.key == K_c:
                    credx = -900
                    credy = -900
                if event.key == K_i:
                    instx = -900
                    insty = -900
                if event.key == K_2:
                    TwoPlayers = True
                if event.key == K_2 or event.key == K_4:
                    for i in range(50):
                        fade = pygame.Surface((1060, 600))
                        fade.set_alpha(i)
                        mixer.music.fadeout(2000)
                        screen.blit(fade, (0, 0))
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    GameRunning = True
                    TitleScreen = False
                    a = 0
                    b = 0

    # When game is running
    while GameRunning:
        if a == 0:
            for i in range(255, 0, -12):
                screen.blit(Floor, (230, 0))
                draw_ship(ship1)
                draw_ship2(ship2)
                if not TwoPlayers:
                    draw_ship3(ship3)
                    draw_ship4(ship4)
                pygame.draw.rect(screen, BLACK, (0, 0, 230, 600))
                pygame.draw.rect(screen, BLACK, (830, 0, 230, 600))
                fade.set_alpha(i)
                screen.blit(fade, (0, 0))
                pygame.display.update()
                fpsClock.tick(FPS)
            P1HP = P2HP = P3HP = P4HP = 10
            Twall.position = Bwall.position = Lwall.position = Rwall.position = (-100, -100)
            a = 1

        if Timer:
            for j in range(3, 0, -1):
                timer = font.render("{}".format(j), True, WHITE)
                screen.blit(Floor, (230, 0))
                draw_ship(ship1)
                draw_ship2(ship2)
                if not TwoPlayers:
                    draw_ship3(ship3)
                    draw_ship4(ship4)
                pygame.draw.rect(screen, BLACK, (0, 0, 230, 600))
                pygame.draw.rect(screen, BLACK, (830, 0, 230, 600))
                screen.blit(timer, (522, 200))
                pygame.display.update()
                fpsClock.tick(FPS)
                time.sleep(1)
            Battle = mixer.music.load('Sounds/battle!.ogg')
            mixer.music.play(-1)
            GameEnded = False
            Timer = False
            b = 1

        screen.blit(Floor, (230, 0))
        calculate_rules()
        key = pygame.key.get_pressed()

        draw_ball(ball)
        draw_ship(ship1)
        draw_ship2(ship2)
        if not TwoPlayers:
            draw_ship3(ship3)
            draw_ship4(ship4)
            screen.blit(Ctrls2, (ctrlsx, ctrlsy))
        else:
            P3HP = 0
            P4HP = 0
            screen.blit(Ctrls, (ctrlsx, ctrlsy))
        pygame.draw.rect(screen, BLACK, (0, 0, 230, 600))
        pygame.draw.rect(screen, BLACK, (830, 0, 230, 600))

        P1S = font.render("Jogador 1: {}".format(P1HP), True, SHIP1)
        P2S = font.render("Jogador 2: {}".format(P2HP), True, SHIP2)
        screen.blit(P1S, (15, 556))
        screen.blit(P2S, (847, 10))

        # Trophies
        if P1Scr > 0:
            trophyx = 55
            screen.blit(Tpy, (trophyx, 495))
            if P1Scr > 1:
                trophyx += 40
                screen.blit(Tpy, (trophyx, 495))
        if P2Scr > 0:
            trophyx2 = 885
            screen.blit(Tpy, (trophyx2, 56))
            if P2Scr > 1:
                trophyx2 += 40
                screen.blit(Tpy, (trophyx2, 56))
        if P3Scr > 0:
            trophyx3 = 55
            screen.blit(Tpy, (trophyx3, 211))
            if P3Scr > 1:
                trophyx3 += 40
                screen.blit(Tpy, (trophyx3, 211))
        if P4Scr > 0:
            trophyx4 = 885
            screen.blit(Tpy, (trophyx4, 322))
            if P4Scr > 1:
                trophyx4 += 40
                screen.blit(Tpy, (trophyx4, 322))

        ship1.position = (ship1Pos[0], 58.1)
        ship2.position = (ship2Pos[0], 2.099)

        if key[pygame.K_LEFT]:
            sSpd1 = -Xmov
            ship1.ApplyLinearImpulse(b2.b2Vec2((sSpd1 * PPM), 0), ship1.position, True)
        elif key[pygame.K_RIGHT]:
            sSpd1 = Xmov
            ship1.ApplyLinearImpulse(b2.b2Vec2((sSpd1 * PPM), 0), ship1.position, True)
        else:
            sSpd1 = 0

        if key[pygame.K_j]:
            sSpd2 = -Xmov
            ship2.ApplyLinearImpulse(b2.b2Vec2((sSpd2 * PPM), 0), ship2.position, True)
        elif key[pygame.K_l]:
            sSpd2 = Xmov
            ship2.ApplyLinearImpulse(b2.b2Vec2((sSpd2 * PPM), 0), ship2.position, True)
        else:
            sSpd2 = 0

        if not TwoPlayers:
            P3S = font.render("Jogador 3: {}".format(P3HP), True, SHIP3)
            P4S = font.render("Jogador 4: {}".format(P4HP), True, SHIP4)
            screen.blit(P3S, (15, 276))
            screen.blit(P4S, (847, 276))
            ship3.position = (25, ship3Pos[1])
            ship4.position = (81, ship4Pos[1])
            if key[pygame.K_q]:
                sSpd3 = -Xmov
                ship3.ApplyLinearImpulse(b2.b2Vec2(0, (sSpd3 * PPM)), ship3.position, True)
            elif key[pygame.K_a]:
                sSpd3 = Xmov
                ship3.ApplyLinearImpulse(b2.b2Vec2(0, (sSpd3 * PPM)), ship3.position, True)
            else:
                sSpd3 = 0
            if key[pygame.K_KP9]:
                sSpd4 = -Xmov
                ship4.ApplyLinearImpulse(b2.b2Vec2(0, (sSpd4 * PPM)), ship4.position, True)
            elif key[pygame.K_KP3]:
                sSpd4 = Xmov
                ship4.ApplyLinearImpulse(b2.b2Vec2(0, (sSpd4 * PPM)), ship4.position, True)
            else:
                sSpd4 = 0

        P1W = font.render('Jogador 1 Venceu!', True, SHIP1)
        P2W = font.render('Jogador 2 Venceu!', True, SHIP2)
        P3W = font.render('Jogador 3 Venceu!', True, SHIP3)
        P4W = font.render('Jogador 4 Venceu!', True, SHIP4)

        if ballY > 613:
            P1HP -= 1
            ball.position = (53, 30)
            ball.ApplyLinearImpulse(b2.b2Vec2((-spdX*PPM), ((-spdY+0.07)*PPM)), ball.position, True)
        if ballY < -13:
            P2HP -= 1
            ball.position = (53, 30)
            ball.ApplyLinearImpulse(b2.b2Vec2((-spdX*PPM), ((spdY-0.07)*PPM)), ball.position, True)
        if ballX < 216:
            P3HP -= 1
            ball.position = (53, 30)
            ball.ApplyLinearImpulse(b2.b2Vec2((-spdX*PPM), ((spdY+0.069)*PPM)), ball.position, True)
        if ballX > 845:
            P4HP -= 1
            ball.position = (53, 30)
            ball.ApplyLinearImpulse(b2.b2Vec2((spdX*PPM), ((-spdY-0.052)*PPM)), ball.position, True)

        if P1HP == 0:
            ship1.position = (53, 66.4)
            Bwall.position = (53, 58.1)
            screen.blit(Vwall, (317, 572))
        if P2HP == 0:
            ship2.position = (53, -6.2)
            Twall.position = (53, 2.1)
            screen.blit(Vwall, (317, 12))
        if P3HP == 0:
            ship3.position = (18, 30)
            Lwall.position = (25, 30)
            screen.blit(Swall, (242, 87))
        if P4HP == 0:
            ship4.position = (97, 30)
            Rwall.position = (81, 30)
            screen.blit(Swall, (802, 87))

        pygame.display.update()

        if (P2HP + P3HP + P4HP) == 0:
            screen.blit(P1W, (390, 220))
            ball.position = (53, 35)
            P1Scr += 1
            GameEnded = True
        elif (P1HP + P3HP + P4HP) == 0:
            screen.blit(P2W, (390, 220))
            ball.position = (53, 35)
            P2Scr += 1
            GameEnded = True
        elif (P1HP + P2HP + P4HP) == 0:
            screen.blit(P3W, (390, 220))
            ball.position = (53, 35)
            P3Scr += 1
            GameEnded = True
        elif (P1HP + P2HP + P3HP) == 0:
            screen.blit(P4W, (390, 220))
            ball.position = (53, 35)
            P4Scr += 1
            GameEnded = True

        if GameEnded:
            ball.position = (53, 30)
            for i in range(50):
                pygame.display.update()
                fpsClock.tick(FPS)
            for i in range(50):
                fade = pygame.Surface((1060, 600))
                fade.set_alpha(i)
                screen.blit(fade, (0, 0))
                pygame.display.update()
                fpsClock.tick(FPS)
            Timer = True
            a = 0

        if P1Scr == 3 or P2Scr == 3 or P3Scr == 3 or P4Scr == 3:
            for i in range(50):
                mixer.music.fadeout(1000)
            GameRunning = False
            TitleScreen = True

        pygame.display.update()
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if b == 0:
                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        c += 1
                        S1 = Skin[c]
                        SHIP1 = TxtSkin[c]

                        if c == 7:
                            c = -1
                    if event.key == K_k:
                        d += 1
                        S2 = Skin[d]
                        SHIP2 = TxtSkin[d]
                        S2 = pygame.transform.rotate(S2, 180)
                        if d == 7:
                            d = -1
                    if event.key == K_s:
                        e += 1
                        S3 = Skin[e]
                        SHIP3 = TxtSkin[e]
                        S3 = pygame.transform.rotate(S3, -90)
                        if e == 7:
                            e = -1
                    if event.key == K_KP6:
                        f += 1
                        S4 = Skin[f]
                        SHIP4 = TxtSkin[f]
                        S4 = pygame.transform.rotate(S4, 90)
                        if f == 7:
                            f = -1
                    if event.key == K_SPACE:
                        Battle = mixer.music.load('Sounds/battle!.ogg')
                        mixer.music.play(-1)
                        ctrlsx = -1000
                        ctrlsy = -1000
                        ball.position = (53, 30)
                        ball.ApplyLinearImpulse(b2.b2Vec2((spdX * PPM), (spdY * PPM)), ball.position, True)
                        b = 1
