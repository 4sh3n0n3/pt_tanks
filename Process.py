import pygame
from Landscape import Land
from weapons.Shell import Shel
from Tank import Tank, Direct
from Net import Server, Client
import ast
from Player import Player
import socket
from time import sleep
from weapons import Bomb, Shell, Saucer, Rocket
from enum import Enum
import enum


class actions(Enum):
    ANGLE_UP = 1
    ANGLE_DOWN = 2
    POWER_UP = 3
    POWER_DOWN = 4
    SHOOT = 5
    MOVE_LEFT = 8
    MOVE_RIGHT = 9


def make_connections():
    choose = input("Пожалуйста, выберите режим, host или guest: ")
    if choose == "host":
        port = input("Выберите порт подключения (оставьте пустым для дефолтного): ")
        sock = Server(port).make_socket()
        return sock, choose

    elif choose == "guest":
        host = input("Введите адрес подключения (оставьте пустым для localhost): ")
        port = input("Выберите порт подключения (оставьте пустым для дефолтного): ")
        sock = Client(host, port).make_socket()
        return sock, choose

    else:
        print("Пожалуйста, проверьте ваш выбор")
        make_connections()


sock, conn_type = make_connections()

shell = Shel()
weapons = [shell]


def start_as_host():
    resX = 800
    resY = 600
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((resX, resY))
    pygame.display.set_caption("HOST")
    color_t1 = (100, 60, 60)
    color_t2 = (60, 100, 100)
    color_l = (80, 180, 10)
    land = Land(screen, color_l, resX, resY)
    tank1 = Tank(screen, color_t1, land=land, weapon_list=weapons)
    tank2 = Tank(screen, color_t2, land=land, weapon_list=weapons)
    tank2.angle = 180
    sock.send((str(resX) + ";" + str(resY) + ";" + str(land.color) + ";" + str(land.road_map) + ";" +
               str(color_t1) + ";" + str(color_t2) + "$").encode('utf8'))
    player = Player(tank1)
    return player, land, tank1, tank2, screen


def start_as_guest():
    data = ""
    while True:
        pack = sock.recv(1024).decode('utf8')
        data += pack
        if "$" in pack:
            break
    data = data.replace("$", "").split(";")
    pygame.display.init()
    pygame.font.init()
    resX = int(data[0].replace('\'(', '').replace('\')', ''))
    resY = int(data[1].replace('\'(', '').replace('\')', ''))
    color_l = ast.literal_eval(data[2])
    color_t1 = ast.literal_eval(data[4])
    color_t2 = ast.literal_eval(data[5])
    screen = pygame.display.set_mode((resX, resY))
    pygame.display.set_caption("GUEST")
    point_dict = ast.literal_eval(data[3])
    land = Land(screen, color_l, resX, resY)
    land.road_map = point_dict
    tank1 = Tank(screen, color_t1, land=land, weapon_list=weapons)
    tank2 = Tank(screen, color_t2, land=land, weapon_list=weapons)
    tank2.angle = 180
    player = Player(tank2)
    return player, land, tank1, tank2, screen


if conn_type == "host":
    player, land, tank1, tank2, screen = start_as_host()
else:
    player, land, tank1, tank2, screen = start_as_guest()

tank1.x, tank1.y = land.box_x // 8, land.box_y // 6
tank2.x, tank2.y = land.box_x // 8 * 7, land.box_y // 6

active_tank = tank1
go = True


def draw_hud(screen):
    font = pygame.font.Font('freesansbold.ttf', 30)
    surf_1 = font.render(str(tank1.points), True, (255, 255, 255))
    surf_1_rect = surf_1.get_rect()
    surf_1_rect.center = (land.box_x // 18, land.box_y // 12)
    screen.blit(surf_1, surf_1_rect)

    surf_2 = font.render(str(tank2.points), True, (255, 255, 255))
    surf_2_rect = surf_2.get_rect()
    surf_2_rect.center = (land.box_x // 18 * 17, land.box_y // 12)
    screen.blit(surf_2, surf_2_rect)

    if player.tank == active_tank:
        own = "Your"
    else:
        own = "Opponent's"

    font = pygame.font.Font('freesansbold.ttf', 20)
    surf_3 = font.render(own + " >> ANGLE : " + str(active_tank.angle) + ", " +
                         "POWER : " + str(active_tank.power) + ", " +
                         "MOVE POINTS LEFT : " + str(active_tank.move_limit), True, (255, 255, 255))
    surf_3_rect = surf_3.get_rect()
    surf_3_rect.center = (land.box_x // 2, land.box_y // 40 * 44)
    screen.blit(surf_3, surf_3_rect)


def render_all():
    land.render()
    tank1.render()
    tank2.render()
    draw_hud(screen)
    weapon = active_tank.weapon_list.pop(0)
    if weapon.push:
        weapon.shoot(active_tank.power, active_tank.angle, active_tank)
        weapon.render(screen, weapon.x, weapon.y)

    pygame.display.flip()



while go:
    render_all()
    pygame.event.pump()
    sock.setblocking(0)
    pressed_list = pygame.key.get_pressed()
    if pressed_list[pygame.K_ESCAPE]:
        go = False

    if player.tank == active_tank:
        if pressed_list[pygame.K_w]:
            active_tank.angle += 1
            if active_tank.angle == 361:
                active_tank.angle = 1
            sock.send(str(actions.ANGLE_UP.value).encode('utf8'))
            sleep(0.05)
        elif pressed_list[pygame.K_s]:
            active_tank.angle -= 1
            if active_tank.angle == -1:
                active_tank.angle = 359
            sock.send(str(actions.ANGLE_DOWN.value).encode('utf8'))
            sleep(0.05)
        elif pressed_list[pygame.K_a]:
            if active_tank.power < 100:
                active_tank.power += 1
                sock.send(str(actions.POWER_UP.value).encode('utf8'))
                sleep(0.05)
        elif pressed_list[pygame.K_d]:
            if active_tank.power > 0:
                active_tank.power -= 1
                sock.send(str(actions.POWER_DOWN.value).encode('utf8'))
                sleep(0.05)
        elif pressed_list[pygame.K_SPACE]:
            sock.send(str(actions.SHOOT.value).encode('utf8'))
            if active_tank == tank1:
                active_tank = tank2
            else:
                active_tank = tank1
            sleep(0.1)
        elif pressed_list[pygame.K_UP]:
            pass
        elif pressed_list[pygame.K_DOWN]:
            pass
        elif pressed_list[pygame.K_LEFT]:
            sock.send(str(actions.MOVE_LEFT.value).encode('utf8'))
            for i in range(0, 30):
                active_tank.move(Direct.LEFT)
                sleep(0.02)
                render_all()
            sleep(0.1)
        elif pressed_list[pygame.K_RIGHT]:
            sock.send(str(actions.MOVE_RIGHT.value).encode('utf8'))
            for i in range(0, 30):
                active_tank.move(Direct.RIGHT)
                sleep(0.02)
                render_all()
            sleep(0.1)

        elif pressed_list[pygame.K_SPACE]:
            sock.send(str(actions.SHOOT.value).encode('utf8'))
            weapon = active_tank.weapon_list.pop(0)
            weapon.push = True
            weapon.x = active_tank.x
            weapon.y = active_tank.y
            weapon.render(screen, weapon.x, weapon.y)



    else:
        try:
            pack = int(sock.recv(1).decode('utf8'))
        except socket.error:
            pack = ''
        if pack == '':
            pass
        elif actions(pack) == actions.ANGLE_UP:
            active_tank.angle += 1
            if active_tank.angle == 361:
                active_tank.angle = 1
        elif actions(pack) == actions.ANGLE_DOWN:
            active_tank.angle -= 1
            if active_tank.angle == -1:
                active_tank.angle = 359
        elif actions(pack) == actions.POWER_UP:
            active_tank.power += 1
        elif actions(pack) == actions.POWER_DOWN:
            active_tank.power -= 1
        elif actions(pack) == actions.SHOOT:
            if active_tank == tank1:
                active_tank = tank2
            else:
                active_tank = tank1
        elif actions(pack) == actions.MOVE_LEFT:
            for i in range(0, 30):
                active_tank.move(Direct.LEFT)
                sleep(0.02)
                render_all()
        elif actions(pack) == actions.MOVE_RIGHT:
            for i in range(0, 30):
                active_tank.move(Direct.RIGHT)
                sleep(0.02)
                render_all()

'''
resX = 800
resY = 600
pygame.display.init()
color_t1 = (100, 60, 60)
color_t2 = (60, 100, 100)
color_l = (80, 180, 10)
screen = pygame.display.set_mode((resX, resY))


land = Land(screen, color_l, resX, resY)
tank1 = Tank(screen, color_t1, land=land)
tank2 = Tank(screen, color_t2, land=land)

tank1_x, tank1_y = 100, 100
tank2_x, tank2_y = 700, 100
go = True
weapon = Shell()

#проверка столкновений
def intersect(x1, x2, y1, y2, w1, w2):
    if (x1 > x2 - w1) and (x1 < x2 + w2) and (y1 > y2 - w1) and (y1 < y2 + w2):
        return 1
    else:
        return 0

while go:
    land.render()
    tank1_x, tank1_y = tank1.render(tank1_x, tank1_y)
    tank2_x, tank2_y = tank2.render(tank2_x, tank2_y)
    pygame.display.flip()
    pygame.event.pump()

for e in pygame.event.get():

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                go = False

            if e.key == pygame.K_SPACE:
                weapon.push = True
                weapon.x = tank1.x + tank1.tube_x
                weapon.y = tank1.y + tank1.tube_y
                weapon.render(screen, weapon.x, weapon.y)
                #tank1.shoot(50, 60, screen)


    if weapon.push:
        weapon.shoot(50, 70, tank1)
        weapon.render(screen, weapon.x, weapon.y)
        pygame.display.flip()

    столкновение орудия с танком
    if intersect(weapon.x, tank2.x, weapon.y, tank2.y, 15, 14) == True:
        weapon.push = False




'''

