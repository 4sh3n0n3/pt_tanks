
import pygame
import time

from weapons.Bomb import Bomb
from weapons.Rocket import Rocket
from weapons.Saucer import Saucer
from weapons.Shell import Shell

pygame.display.init()
M = 800
N = 800
window = pygame.display.set_mode((M, N))
pygame.display.set_caption('Pocket Tanks')
screen = pygame.Surface((800, 800))

eapon = Shell(0, 0)


done = True
while done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False

    screen.fill((0, 55, 0))
    eapon.render(screen)
    window.blit(screen, (0, 0))
    pygame.display.flip()


