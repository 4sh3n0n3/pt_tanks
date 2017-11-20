import pygame
from Net import Server, Client
import socket
from time import sleep
from enum import Enum
from Render import Render
import Ivent


class actions(Enum):
    ANGLE_UP = 1
    ANGLE_DOWN = 2
    POWER_UP = 3
    POWER_DOWN = 4
    SHOOT = 5
    NEXT_GUN = 6
    PREV_GUN = 7
    MOVE_LEFT = 8
    MOVE_RIGHT = 9


def make_connections():
    choose = input("Пожалуйста, выберите режим, host или guest: ")
    if choose == "host":
        port = input("Выберите порт подключения (оставьте пустым для дефолтного): ")
        socket = Server(port).make_socket()
        return socket, choose

    elif choose == "guest":
        host = input("Введите адрес подключения (оставьте пустым для localhost): ")
        port = input("Выберите порт подключения (оставьте пустым для дефолтного): ")
        socket = Client(host, port).make_socket()
        return socket, choose


sock, conn_type = make_connections()


if conn_type == "host":
    self_player, enemy_player = Ivent.start_as_host(sock)
    active_player = self_player
    renderer = Render(self_player, enemy_player)
else:
    enemy_player, self_player = Ivent.start_as_guest(sock)
    active_player = enemy_player
    renderer = Render(enemy_player, self_player)


Ivent.init(renderer)
active_player.tank.x, active_player.tank.y = active_player.land.box_x // 8, active_player.land.box_y // 6
active_player.enemy.x, active_player.enemy.y = active_player.land.box_x // 8 * 7, active_player.land.box_y // 6
go = True


while go:
    if self_player == active_player:
        isActive = True
    else:
        isActive = False

    renderer.render_all(self_player, isActive)
    pygame.event.pump()
    sock.setblocking(0)
    pressed_list = pygame.key.get_pressed()

    if pressed_list[pygame.K_ESCAPE]:
        go = False

    if self_player == active_player:
        if pressed_list[pygame.K_w]:
            Ivent.angle_up(active_player)
            sock.send(str(actions.ANGLE_UP.value).encode('utf8'))
            sleep(0.05)

        elif pressed_list[pygame.K_s]:
            Ivent.angle_down(active_player)
            sock.send(str(actions.ANGLE_DOWN.value).encode('utf8'))
            sleep(0.05)

        elif pressed_list[pygame.K_a]:
            Ivent.power_up(active_player)
            sock.send(str(actions.POWER_UP.value).encode('utf8'))
            sleep(0.1)

        elif pressed_list[pygame.K_d]:
            Ivent.power_down(active_player)
            sock.send(str(actions.POWER_DOWN.value).encode('utf8'))
            sleep(0.05)

        elif pressed_list[pygame.K_SPACE]:
            sock.send(str(actions.SHOOT.value).encode('utf8'))
            if not active_player.tank.weapon_list:
                break
            Ivent.shoot(active_player, self_player)

            active_player = enemy_player
            sleep(0.1)

        elif pressed_list[pygame.K_UP]:
            Ivent.switch_gun_up(active_player)
            sleep(0.1)
            sock.send(str(actions.NEXT_GUN.value).encode('utf8'))

        elif pressed_list[pygame.K_DOWN]:
            Ivent.angle_down(active_player)
            sleep(0.1)
            sock.send(str(actions.PREV_GUN.value).encode('utf8'))

        elif pressed_list[pygame.K_LEFT]:
            sock.send(str(actions.MOVE_LEFT.value).encode('utf8'))
            Ivent.move_left(active_player, self_player)
            sleep(0.1)

        elif pressed_list[pygame.K_RIGHT]:
            sock.send(str(actions.MOVE_RIGHT.value).encode('utf8'))
            Ivent.move_right(active_player, self_player)
            sleep(0.1)
    else:
        try:
            pack = sock.recv(1).decode('utf8')
            if pack != '':
                pack = int(pack)
        except socket.error:
            pack = ''

        if pack == '':
            pass

        elif actions(pack) == actions.ANGLE_UP:
            Ivent.angle_up(active_player)

        elif actions(pack) == actions.ANGLE_DOWN:
            Ivent.angle_down(active_player)

        elif actions(pack) == actions.POWER_UP:
            Ivent.power_up(active_player)

        elif actions(pack) == actions.POWER_DOWN:
            Ivent.angle_down(active_player)

        elif actions(pack) == actions.SHOOT:
            if not active_player.tank.weapon_list:
                break
            Ivent.shoot(active_player, self_player)

            active_player = self_player

        elif actions(pack) == actions.NEXT_GUN:
            Ivent.switch_gun_up(active_player)

        elif actions(pack) == actions.PREV_GUN:
            Ivent.switch_gun_down(active_player)

        elif actions(pack) == actions.MOVE_LEFT:
            Ivent.move_left(active_player, self_player)

        elif actions(pack) == actions.MOVE_RIGHT:
            Ivent.move_right(active_player, self_player)

sock.close()
if self_player.tank.points > self_player.enemy.points:
    renderer.endgame(self_player, "You win!")
    sleep(2)
elif self_player.tank.points < self_player.enemy.points:
    renderer.endgame(self_player, "You lose!")
    sleep(2)
else:
    renderer.endgame(self_player, "Dead heat")
    sleep(2)

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
while go:
    land.render()
    tank1_x, tank1_y = tank1.render(tank1_x, tank1_y)
    tank2_x, tank2_y = tank2.render(tank2_x, tank2_y)
    pygame.display.flip()
    pygame.event.pump()

    pressed_list = pygame.key.get_pressed()
    if pressed_list[pygame.K_ESCAPE]:
        go = False
'''
