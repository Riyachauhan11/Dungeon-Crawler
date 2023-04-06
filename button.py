import pygame
import constants as const

class Button():


    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hover_col=const.HOVER

    def draw(self, surface):
        action = False
        surface.blit(self.image, self.rect)

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse is over button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action = True
                pygame.draw.rect(surface, self.hover_col, self.rect,10)
            else:
                pygame.draw.rect(surface, self.hover_col, self.rect,10)


        return action
