import pygame
from weapons.IWeapon import Weapon

#бомба
class Bomb(Weapon):
    DAMAGE = 22

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bitmap = pygame.image.load('sprites/bomb.png')

    def render(self, screen):
        self.bitmap = pygame.transform.scale(self.bitmap, (65, 50))
        self.rect = pygame.Rect(0, 0, 65, 50)
        screen.blit(self.bitmap, (self.x, self.y))

    def shoot(self):
        pass