import pygame
import math as m
from weapons.IWeapon import Weapon
from Player import Player


# снаряд
class Shell(Weapon):
    DAMAGE = 20
    RAD = 50

    def __init__(self):
        self.start = True
        self.x = 1
        self.y = 1
        self.xK = 0
        self.yK = 0
        self.y_speed = 0
        self.bitmap = pygame.image.load('weapons/sprites/shell.png')

    def render(self, screen):
        self.bitmap = pygame.transform.scale(self.bitmap, (15, 15))
        screen.blit(self.bitmap, (self.x, self.y))

    def shoot(self, power, angle, tank, screen):
        if self.start:
            self.x = int(tank.x - 1 + 15 * m.cos(m.radians(tank.angle)))
            self.y = int(tank.y - 15 * m.sin(m.radians(tank.angle)))
            self.render(screen)
            self.start = False

        else:
            self.xK += 1
            # уравнение параболической траектории
            self.yK = self.xK * m.fabs(m.tan(m.radians(angle))) - 9.8 * self.xK * self.xK / (
            2 * power * power * m.cos(m.radians(angle)) * m.cos(m.radians(angle)))

            if angle < 90 or angle > 270:

                self.x += self.xK
                self.y = self.y - self.yK

            else:

                self.x -= self.xK
                self.y = self.y - self.yK

            self.render(screen)

    def boom(self, screen, tank1, tank2):
        self.start = True
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.RAD)
        x_1, y_1 = self.x - tank1.hitbox[0], self.y - tank1.hitbox[1]
        p_1 = [(x_1, y_1), (x_1 + 14, y_1), (x_1, y_1 + 8), (x_1 + 15, y_1 + 8)]
        x_2, y_2 = self.x - tank2.hitbox[0], self.y - tank2.hitbox[1]
        p_2 = [(x_2, y_2), (x_2 + 14, y_2), (x_2, y_2 + 8), (x_2 + 15, y_2 + 8)]

        trig_1 = False
        trig_2 = False
        for point in p_1:
            if m.sqrt(point[0]**2 + point[1]**2) <= self.RAD:
                trig_1 = True

        for point in p_2:
            if m.sqrt(point[0]**2 + point[1]**2) <= self.RAD:
                trig_2 = True

        if trig_1:
            tank1.points -= self.DAMAGE
        if trig_2:
            tank2.points -= self.DAMAGE

    def collision_detection(self, player):
        if self.x < 0 or self.x > player.land.box_x or self.y > player.land.box_y:
            return False
        try:
            y = player.land.road_map.get(int(self.x))[1]
        except Exception:
            y = player.land.box_y
        if self.y < y and 0 < self.x < player.land.box_x:
            return True
        else:
            return False
