import pygame

from weapons.IWeapon import Weapon


class Rocket(Weapon):
    DAMAGE = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bitmap = pygame.image.load('sprites/rocket.png')

    def render(self, screen):
        self.bitmap = pygame.transform.scale(self.bitmap, (50, 50))
        self.rect = pygame.Rect(0, 0, 50, 50)
        screen.blit(self.bitmap, (self.x, self.y))

    def shoot(self):
        pass