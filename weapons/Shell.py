import pygame
import math
from weapons.IWeapon import Weapon

#снаряд
class Shell(Weapon):
    DAMAGE = 10


    def __init__(self):
        self.push = False
        self.x = 1
        self.y = 1
        self.bitmap = pygame.image.load('weapons/sprites/shell.png')

    def render(self, screen, x, y):
        self.bitmap = pygame.transform.scale(self.bitmap, (15, 15))
        #self.rect = pygame.Rect(self.x, self.y, 50, 50)
        screen.blit(self.bitmap, (x, y))


    def shoot(self, power, angle, tank):
        if self.x > 800: #пока не улетел за экран
            self.push = False

        #установка снаряда в дуло танка
        if self.push == False:
            self.x = tank.x + tank.tube_x
            self.y = tank.y + tank.tube_y
        else:
            self.x += 4
            angle = math.radians(angle)
            # уравнение параболической траектории
            k = (self.x * math.tan(angle) - 9.8 * self.x * self.x / (2 * power * power - math.cos(angle) * math.cos(angle)))
            self.y = (tank.y + tank.tube_y) - k + (tank.y)/2



