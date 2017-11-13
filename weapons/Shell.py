import pygame
import math as m
from weapons.IWeapon import Weapon


# снаряд
class Shell(Weapon):
    DAMAGE = 20
    RAD = 50

    def __init__(self):
        self.start = True
        self.x = 1
        self.y = 1
        self.bitmap = pygame.image.load('weapons/sprites/shell.png')

    def render(self, screen):
        self.bitmap = pygame.transform.scale(self.bitmap, (15, 15))
        screen.blit(self.bitmap, (self.x, self.y))

    def shoot(self, power, angle, tank, screen):
        # установка снаряда в дуло танка
        if self.start:
            self.x = int(tank.x - 1 + 15 * m.cos(m.radians(tank.angle)))
            self.y = int(tank.y - 15 * m.sin(m.radians(tank.angle)))
            self.render(screen)
            self.start = False
        else:
            self.x += 4
            angle = m.radians(angle)
            # уравнение параболической траектории
            k = (self.x * m.tan(angle) - 9.8 * self.x * self.x / (2 * power * power - m.cos(angle) * m.cos(angle)))
            self.y = (tank.y - 15 * m.sin(m.radians(tank.angle))) - k + tank.y / 2
            self.render(screen)
        return self.x, self.y

    def boom(self, screen, tank1, tank2):
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
                trig_1 = True

        if trig_1:
            tank1.points -= self.DAMAGE
        if trig_2:
            tank2.points -= self.DAMAGE