import pygame
import math as m


class Tank:
    def __init__(self, screen, color, land, weapon_list=[]):
        self.screen = screen
        self.color = color
        self.x = 0
        self.y = 0
        self.weapon_list = weapon_list
        self.points = 0
        self.angle = 0
        self.power = 50
        self.hitbox = (self.x-5, self.y-3, 10, 6)
        self.land = land

    def render(self, x, y):
        tube_x = 15 * m.cos(m.radians(self.angle))
        tube_y = - 15 * m.sin(m.radians(self.angle))
        # tube_x, tube_y = rotate_coords(x=8, cos=m.cos(m.radians(self.angle)), sin=m.sin(m.radians(self.angle)))

        land_left, land_right = self.land.road_map.get(x-7), self.land.road_map.get(x+7)

        gip_len = m.sqrt((land_right[0]-land_left[0])**2+(land_right[1]-land_left[1])**2)
        box_cos = (land_left[1]-land_right[1])/gip_len
        box_sin = 14/gip_len

        # Заглушка. Здесь будет реализована физика равноускоренного падения
        # (передавать какой-нибудь аргумент power для обработки)
        if self.land.road_map.get(x)[1] > y+5:
            y = y + 2

        update_hitbox(self, x, y)

        pygame.draw.aaline(self.screen, (200, 200, 200), (self.x-1, self.y), (self.x - 1 + tube_x, self.y + tube_y))
        print(round(rotate_coords(self.x-7, self.y-4, box_cos, box_sin)[0]), round(rotate_coords(self.x-7, self.y-4, box_cos, box_sin)[1]))
        print("not rot", self.x-7, self.y-4)
        pygame.draw.polygon(self.screen, self.color, [(self.x-7, self.y-4),
                                                      (self.x+7, self.y-4),
                                                      (self.x+10, self.y+4),
                                                      (self.x-10, self.y+4)])

        return x, y


def rotate_coords(x=0, y=0, cos=0.0, sin=0.0):
    x_ret = x + x*cos + y*sin
    y_ret = y - x*sin + y*cos
    return x_ret, y_ret


def update_hitbox(tank, x, y, box_angle=0):
    TANK_LENGTH = 14
    TANK_HEIGHT = 8
    tank.x = x
    tank.y = y

    tank.hitbox = (x-7, y-4, 14, 8)


# FOR TESTING
'''
go = True
resX = 800
resY = 600
pygame.display.init()
color = (100, 60, 60)
screen = pygame.display.set_mode((resX, resY))
tanka = Tank(screen, color)

while go:
    tanka.render(400, 300)
    pygame.display.flip()
    pygame.event.pump()

    pressed_list = pygame.key.get_pressed()
    if pressed_list[pygame.K_ESCAPE]:
        go = False
'''
