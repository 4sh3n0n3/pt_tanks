import pygame
from Landscape import Land
from Tank import Tank
from weapons.Shell import Shell

go = True
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
weapon = Shell()

#проверка столкновений
def intersect(x1, x2, y1, y2, w1, w2):
    if (x1 > x2 - w1) and (x1 < x2 + w2) and (y1 > y2 - w1) and (y1 < y2 + w2):
        return 1
    else:
        return 0

while go:
    land.render()
    tank1_x, tank1_y = tank1.render(tank1_x, tank1_y)
    tank2_x, tank2_y = tank2.render(tank2_x, tank2_y)
    pygame.display.flip()
    pygame.event.pump()

    for e in pygame.event.get():

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                go = False

            if e.key == pygame.K_SPACE:
                weapon.push = True
                weapon.x = tank1.x + tank1.tube_x
                weapon.y = tank1.y + tank1.tube_y
                weapon.render(screen, weapon.x, weapon.y)
                #tank1.shoot(50, 60, screen)


    if weapon.push:
        weapon.shoot(50, 70, tank1)
        weapon.render(screen, weapon.x, weapon.y)
        pygame.display.flip()

    '''столкновение орудия с танком'''
    if intersect(weapon.x, tank2.x, weapon.y, tank2.y, 15, 14) == True:
        weapon.push = False



