
import pygame
import time

from weapons.Bomb import Bomb
from weapons.Rocket import Rocket
from weapons.Saucer import Saucer
from weapons.Shell import Shell

pygame.display.init()
M = 1600
N = 800
window = pygame.display.set_mode((M, N))
pygame.display.set_caption('Pocket Tanks')
screen = pygame.Surface((1600, 800))

weapon = Shell(100, 300)
weapon.push = False

done = True
pygame.key.set_repeat(1,1)
while done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False



        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if weapon.push == False:
                    weapon.push = True

    screen.fill((0, 55, 0))

    weapon.shoot(2, 65)

    weapon.render(screen)
    window.blit(screen, (0, 0))
    pygame.display.flip()




