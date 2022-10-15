import pygame, random
from Settings import *
import os
from math import sin, pi, cos
pygame.init()
from ManagersAndMenus import render_fixwidth_text, BMBuilder

class Catroom(BMBuilder):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)

        
        self.strikethrough_surf = pygame.transform.smoothscale(pygame.image.load(r'images\strikethrough.png'), (1773//10.5, 245//10.5))
        self.strikethrough_rect = self.strikethrough_surf.get_rect()
        self.strikethrough_rect.center = 225, 45
        
        self.catchat_textsurf = pygame.font.Font('fonts\\pico.ttf', 40).render('Catroom', True, ((54, 151, 255)))
        self.catchat_textrect = self.catchat_textsurf.get_rect()
        self.catchat_textrect.center = 225, 78
        
        self.beta = pygame.transform.smoothscale(pygame.image.load(r'images\icons\beta.png'), (290//8, 188/8))
    
    def draw(self):
        pass
        # self.screen.blit(self.strikethrough_surf, self.strikethrough_rect)
        # self.screen.blit(self.catchat_textsurf, self.catchat_textrect)
        self.screen.blit(self.beta, (self.catchat_textrect.topright[0]-20, self.catchat_textrect.topright[1]))