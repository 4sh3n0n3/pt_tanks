import pygame


class Render:
    def __init__(self, host, guest):
        self.player1 = host
        self.player2 = guest

    def draw_points(self, player):
        left_points = self.player1.tank.points
        right_points = self.player2.tank.points

        font = pygame.font.Font('freesansbold.ttf', 30)
        surf_1 = font.render(str(left_points), True, (255, 255, 255))
        surf_1_rect = surf_1.get_rect()
        surf_1_rect.center = (player.land.box_x // 18, player.land.box_y // 12)
        player.screen.blit(surf_1, surf_1_rect)

        surf_2 = font.render(str(right_points), True, (255, 255, 255))
        surf_2_rect = surf_2.get_rect()
        surf_2_rect.center = (player.land.box_x // 18 * 17, player.land.box_y // 12)
        player.screen.blit(surf_2, surf_2_rect)

    def draw_hud(self, player, isActive):
        self.draw_points(player)

        if isActive:
            own = "Your"
        else:
            own = "Opponent's"

        font = pygame.font.Font('freesansbold.ttf', 20)
        surf_3 = font.render(own + " >> ANGLE : " + str(player.tank.angle) + ", " +
                             "POWER : " + str(player.tank.power) + ", " +
                             "MOVE POINTS LEFT : " + str(player.tank.move_limit), True, (255, 255, 255))
        surf_3_rect = surf_3.get_rect()
        surf_3_rect.center = (player.land.box_x // 2, player.land.box_y // 40 * 44)
        player.screen.blit(surf_3, surf_3_rect)

    def render_all(self, player, isActive):
        player.land.render()
        player.tank.render()
        player.enemy.render()
        self.draw_hud(player, isActive)
        pygame.display.flip()

    def endgame(self, player, result):
        player.screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 30)
        surf = font.render(result, True, (255, 255, 255))
        surf_rect = surf.get_rect()
        surf_rect.center = (player.land.box_x//2, player.land.box_y//2)
        player.screen.blit(surf, surf_rect)
        pygame.display.flip()
