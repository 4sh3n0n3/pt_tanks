from time import sleep
from Tank import Direct
import pygame
from Player import Player
from Landscape import Land
from Tank import Tank
import ast
from weapons.Shell import Shell


renderer = None


def init(render):
    global renderer
    renderer = render


def angle_up(active_player):
    active_player.tank.angle += 1
    if active_player.tank.angle == 361:
        active_player.tank.angle = 1


def angle_down(active_player):
    active_player.tank.angle -= 1
    if active_player.tank.angle == -1:
        active_player.tank.angle = 359


def power_up(active_player):
    if active_player.tank.power < 100:
        active_player.tank.power += 1


def power_down(active_player):
    if active_player.tank.power > 0:
        active_player.tank.power -= 1


def shoot(active_player, self_player):
    if active_player == self_player:
        isActive = True
    else:
        isActive = False

    weapon = active_player.tank.weapon_list.pop(active_player.tank.selected_gun)
    weapon.shoot(active_player.tank.power, active_player.tank.angle, active_player.tank, self_player.screen)
    pygame.display.flip()
    while weapon.collision_detection(active_player):
        weapon.shoot(active_player.tank.power, active_player.tank.angle, active_player.tank, self_player.screen)
        pygame.display.flip()
        sleep(0.05)
        renderer.render_all(self_player, isActive)
    weapon.boom(self_player.screen, active_player.tank, active_player.enemy)
    pygame.display.flip()
    sleep(1.5)
    renderer.render_all(self_player, isActive)
    active_player.tank.selected_gun = 0
    sleep(0.1)


def switch_gun_up(active_player):
    if active_player.tank.selected_gun < len(active_player.tank.weapon_list) - 1:
        active_player.tank.selected_gun += 1
    else:
        active_player.tank.selected_gun = 0


def switch_gun_down(active_player):
    if active_player.tank.selected_gun > 0:
        active_player.tank.selected_gun -= 1
    else:
        active_player.tank.selected_gun = len(active_player.tank.weapon_list) - 1


def move_left(active_player, self_player):
    if active_player == self_player:
        isActive = True
    else:
        isActive = False
    for i in range(0, 30):
        active_player.tank.move(Direct.LEFT)
        sleep(0.02)
        renderer.render_all(self_player, isActive)
    sleep(0.1)


def move_right(active_player, self_player):
    if active_player == self_player:
        isActive = True
    else:
        isActive = False
    for i in range(0, 30):
        active_player.tank.move(Direct.RIGHT)
        sleep(0.02)
        renderer.render_all(self_player, isActive)
    sleep(0.1)


def load_weapons():
    shell_1 = Shell()
    shell_2 = Shell()
    shell_3 = Shell()
    weapons = [shell_1, shell_2, shell_3]
    return weapons


def start_as_host(sock):
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
    tank1 = Tank(screen, color_t1, land=land, weapon_list=load_weapons())
    tank2 = Tank(screen, color_t2, land=land, weapon_list=load_weapons())
    tank2.angle = 180
    sock.send((str(resX) + ";" + str(resY) + ";" + str(land.color) + ";" + str(land.road_map) + ";" +
               str(color_t1) + ";" + str(color_t2) + "$").encode('utf8'))
    player1 = Player(tank1, land, screen, tank2)
    player2 = Player(tank2, land, screen, tank1)
    return player1, player2


def start_as_guest(sock):
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
    tank1 = Tank(screen, color_t1, land=land, weapon_list=load_weapons())
    tank2 = Tank(screen, color_t2, land=land, weapon_list=load_weapons())
    tank2.angle = 180
    player1 = Player(tank1, land, screen, tank2)
    player2 = Player(tank2, land, screen, tank1)
    return player1, player2