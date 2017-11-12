import pygame
from Landscape import Land
from Tank import Tank
from Net import Server, Client
import ast


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


def start_as_host():
    resX = 800
    resY = 600
    pygame.display.init()
    screen = pygame.display.set_mode((resX, resY))
    color_t1 = (100, 60, 60)
    color_t2 = (60, 100, 100)
    color_l = (80, 180, 10)
    land = Land(screen, color_l, resX, resY)
    tank1 = Tank(screen, color_t1, land=land)
    tank2 = Tank(screen, color_t2, land=land)
    sock.sendall((str(resX) + ";" + str(resY) + ";" + str(land.color) + ";" + str(land.road_map) + ";" +
                  str(color_t1) + ";" + str(color_t2)).encode('utf8'))
    return land, tank1, tank2


def str_tuple_to_int(tup):
    for i in range(0, len(tup)):
        tup[i] = int(tup[i])


def start_as_guest():
    data = ""
    while True:
        pack = sock.recv(1024).decode('utf8')
        data += pack
        if not pack:
            break
    data = data.split(";")
    pygame.display.init()
    resX = int(data[0].replace('\'(', '').replace('\')', ''))
    resY = int(data[1].replace('\'(', '').replace('\')', ''))
    color_l = ast.literal_eval(data[2])
    color_t1 = ast.literal_eval(data[4])
    color_t2 = ast.literal_eval(data[5])
    screen = pygame.display.set_mode((resX, resY))
    point_dict = ast.literal_eval(data[3])
    land = Land(screen, color_l, resX, resY)
    land.road_map = point_dict
    tank1 = Tank(screen, color_t1, land=land)
    tank2 = Tank(screen, color_t2, land=land)
    return land, tank1, tank2


if conn_type == "host":
    land, tank1, tank2 = start_as_host()
else:
    land, tank1, tank2 = start_as_guest()


tank1_x, tank1_y = land.box_x//8, 100
tank2_x, tank2_y = land.box_x//8*7, 100
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