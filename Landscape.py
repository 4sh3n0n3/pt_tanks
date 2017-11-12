import pygame
import random


class Land:
    def __init__(self, screen, color, box_x, box_y):
        self.screen = screen
        self.color = color
        self.box_x = box_x
        self.box_y = box_y-box_y//10
        self.road_map = generate_landscape(box_x, box_y)

    def render(self):
        self.screen.fill((0, 0, 0))
        for point in self.road_map.values():
            pygame.draw.aaline(self.screen, self.color, point, (point[0], self.box_y))


def generate_landscape(max_x, max_y):
    mapping = []
    dict = {}

    # Генерация ломаной
    for x in range(0, max_x):
        y = random.randrange((max_y//2)-max_y//6, (3*max_y//2)-max_y//2)
        point = [x, y]
        mapping.append(point)

    # Генерация горы
    for x in range(max_x//3, 2*max_x//3):
        if x < max_x//2:
            mapping[x][1] = mapping[x][1] - random.randrange(x//5, x//2)
        if x > max_x//2:
            if random.randrange(0, 2) == 0:
                val = mapping[max_x - x][1]
            else:
                val = mapping[x][1]
            mapping[x][1] = val - random.randrange((max_x - x)//5, (max_x - x)//2)

    # Снижение резкости
    for x in range(0, max_x):
        val = mapping[x][1]
        prevval = mapping[x-1][1]
        if val - prevval > 3:
            mapping[x][1] = val - (val - prevval) + 3

    # Выравнивание
    for x in range(0, max_x):
        val = mapping[x][1]
        prevval = mapping[x-1][1]
        if abs(val - prevval) < 20:
            mapping[x][1] = prevval

    # Сглаживание
    for k in range(0, 6):
        for i in range(0, max_x):
            sr_sum = 0
            for j in range(0, 15):
                x = i+j
                if i+j >= max_x:
                    x = i+j - max_x
                sr_sum += mapping[x][1]
            sr_sum //= 15
            mapping[i][1] = sr_sum + max_y//25
    for point in mapping:
        adder = {point[0]: point}
        dict.update(adder)

    return dict


# FOR TESTING
'''
go = True
resX = 800
resY = 600
pygame.display.init()
color = (80, 180, 10)
screen = pygame.display.set_mode((resX, resY))
land = Land(screen, color, resX, resY)
while go:
    land.render()
    pygame.display.flip()
    pygame.event.pump()

    pressed_list = pygame.key.get_pressed()
    if pressed_list[pygame.K_ESCAPE]:
        go = False
'''
