import pygame, random
from Settings import *
import os
from math import sin, pi, cos
pygame.init()
from ManagersAndMenus import render_fixwidth_text, BMBuilder
# import socket
# import threading

class TextBox:
    def __init__(self, rect, font = pygame.font.SysFont('Calibri', 20)):
        
        self.textbox = rect
        self.text_font = font
        self.text = ''
        self.render_text = lambda: render_fixwidth_text(self.text, self.text_font, self.textbox.width-10, (255, 255, 255))
    
    def draw(self, screen):
        pygame.draw.rect(screen, HIGHLIGHT_COL, self.textbox, width=2, border_radius=self.textbox.height//2)    # Text Box Outer
        if self.text != '': 
            screen.blit(self.text_surf, (self.textbox.midleft[0]+self.textbox.height/2, self.textbox.topleft[1] + 4))

    def keydown(self, event):
        print(event)
        if event.key == 13:  
            self.text = ''
            return True   # If enter is pressed  
        
        elif event.key == 8:         # If backspace is pressed
            if event.mod == 4160:    # Ctrl + Backspace
                self.text = ' '.join(self.text.split()[:-1])
            else: self.text = self.text[:-1]
            self.text_surf = self.render_text()
            
        else:
            self.text += event.unicode
            self.text_surf = self.render_text()
    
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

        # Text interface
        self.send_icon = pygame.transform.smoothscale(pygame.image.load(r'images\icons\send.png'), (50, 50))
        self.send_rect = self.send_icon.get_rect()
        self.send_rect.bottomright = WIDTH-10, HEIGHT-10
        
        self.textbox = TextBox(pygame.Rect(5, HEIGHT-60, WIDTH-10-60, 50))
        
        
    def draw(self):
        self.screen.blit(self.beta, (self.catchat_textrect.topright[0]-20, self.catchat_textrect.topright[1]))         # Beta icon
        self.textbox.draw(self.screen)
        self.screen.blit(self.send_icon, self.send_rect)                                                               # Send Button
        
        
    def keydown(self, event):
        if self.textbox.keydown(event):
            self.send_msg()
    
    def send_msg(self):
        print(self.textbox.text)
    
    def click(self, pos):
        if self.send_rect.collidepoint(pos):
            self.send_msg()
        