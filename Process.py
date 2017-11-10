import pygame
from Landscape import Land
from Tank import Tank

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
while go:
    land.render()
    tank1_x, tank1_y = tank1.render(tank1_x, tank1_y)
    tank2_x, tank2_y = tank2.render(tank2_x, tank2_y)
    pygame.display.flip()
    pygame.event.pump()

    pressed_list = pygame.key.get_pressed()
    if pressed_list[pygame.K_ESCAPE]:
        go = False
