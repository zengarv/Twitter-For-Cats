import os
import random

import pygame

from Settings import *

pygame.init()
import socket
import threading
from datetime import datetime

from fireworks import r_c
from ManagersAndMenus import BMBuilder, render_fixwidth_text


class TextBox:        
    def __init__(self, rect:pygame.Rect, font = pygame.font.SysFont('Calibri', 20)):      
        self.textbox = rect
        self.text_font = font
        self.text = ''
        
        corner_radius = rect.height//2
        h_padding = 2
        v_padding = 4
        self.text_mask = pygame.Rect(rect.left+corner_radius+h_padding, rect.top+v_padding, rect.width-2*(corner_radius + h_padding), rect.height-2*v_padding)
        self.multiline = False
        
        self.no_text_surf = font.render('Type your message', True, (60, 60, 60))
        self.no_text_surf_rect = self.no_text_surf.get_rect()
        self.no_text_surf_rect.midleft = self.text_mask.left, self.textbox.centery
        
    def render_text(self): 
        surf = render_fixwidth_text(self.text, self.text_font, self.text_mask.width, (255, 255, 255), linespace=5)
        self.text_rect = surf.get_rect()
        self.multiline = self.text_mask.height < self.text_rect.height
        h = min(self.text_rect.height, self.text_mask.height)
        return surf.subsurface((0, self.text_rect.height - h, self.text_rect.width, h))
    
    def draw(self, screen):
        # pygame.draw.rect(screen, tweet_bg_col, self.textbox) 
        pygame.draw.rect(screen, HIGHLIGHT_COL, self.textbox, width=1, border_radius=self.textbox.height//2)    # Text Box Outer
        if len(self.text.strip()) != 0: 
            if self.multiline:
                screen.blit(self.text_surf, self.text_mask)
            else:
                self.text_rect.midleft = self.text_mask.left, self.textbox.centery
                screen.blit(self.text_surf, self.text_rect)
        else:
            screen.blit(self.no_text_surf, self.no_text_surf_rect)
        
    def keydown(self, event):
        if event.key == 13 and len(self.text.strip()) > 0:  
            self.last_text = self.text
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

class Message:
    def __init__(self, text, top, user='You', user_col=(100, 240, 80)) -> None:
        self.text = text
        self.user = user
        
        # Drawing the surface of the message      
        text_surf = render_fixwidth_text(text, message_font, WIDTH-10-20, (230, 230, 230), linespace=5)
        text_rect = text_surf.get_rect()
        user_surf = message_font.render(user, True, user_col)
        user_rect = user_surf.get_rect()
        time_surf = time_font.render(datetime.now().strftime('%H:%M'), True, (80, 80, 80))
        time_rect = time_surf.get_rect()

        h_padding = 10
        v_padding = 4
        
        user_rect.topleft = h_padding, v_padding
        text_rect.topleft = h_padding, user_rect.bottom+v_padding
        
        self.surf = pygame.Surface((WIDTH, text_rect.bottom+v_padding))
        self.rect = self.surf.get_rect()
        
        self.surf.fill(tweet_bg_col)
        self.surf.blit(user_surf, user_rect)
        self.surf.blit(text_surf, text_rect)
        
        time_rect.bottomright = self.rect.right - 4, self.rect.bottom-4
        self.surf.blit(time_surf, time_rect)

        pygame.draw.rect(self.surf, (30, 30, 30), self.rect, 1, 5)
        
        self.rect.top = top        
        
    def draw(self, screen):
        screen.blit(self.surf, self.rect)

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
        
        self.textbox = TextBox(pygame.Rect(5, HEIGHT-60, WIDTH-10-70, 50))
        
        # Message Handling
        self.messages = []
        self.message_space = pygame.Rect(0, 100, WIDTH, HEIGHT-100-65)

        # Scrolling
        self.scroll_vel = 0
        self.scroll_resistance = 1           # Lower for smoother scrolling, higher for better performance
        self.max_scroll_vel = 50
        
        # Messaging - Socket Stuff
        self.connection_established = False
        
        self.conn_lost_surf = pygame.transform.smoothscale(pygame.image.load(r'images\icons\connectionlost.png'), (240, 240))
        self.conn_lost_rect = self.conn_lost_surf.get_rect()
        self.conn_lost_rect.center = WIDTH/2, HEIGHT/2
        self.conn_lost_text = render_fixwidth_text("Connection to the server could not be established. Type '!reconnect' to attempt a reconnection.", pygame.font.SysFont('Calibri', 30), 550, (230, 230, 230), linespace=7)
        self.clt_rect = self.conn_lost_text.get_rect()
        self.clt_rect.midtop = WIDTH/2, self.conn_lost_rect.bottom + 20
        
        self.username = 'Ket'
        self.attempt_connection()
    
        self.username_surf = pygame.font.SysFont('Avant Garde', 24).render(f'{self.username}', True, (100, 240, 80))
        self.username_rect = self.username_surf.get_rect()
        self.username_rect.topright = WIDTH-10, 75
        self.username_box = self.username_rect.inflate(12, 6)
        
        self.msg_recieve_sound = mixer.Sound(r'sounds/msg_recieve.wav')
        self.msg_send_sound = mixer.Sound(r'sounds/msg_send.wav')
        self.you_got_a_text = mixer.Sound(r'sounds/you_got_a_text.wav')
        
        self.focused = False
        
    def attempt_connection(self):
        if not self.connection_established:
            print("[CONNECTING]: Attempting connection to server...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(ADDR)
                print(f'[CONNECTION]: Connection Successful')
                
                self.recieve_msgs = True
                self.reciever = threading.Thread(target=self.recieve)
                self.reciever.start()
                
                self.users = {}  # Key: username [str], Value: color
                self.username = random.choice([usernames.at[random.randint(0, len(usernames.index)-1), 'Handles'], usernames.at[random.randint(0, len(usernames.index)-1), 'Adj'] + usernames.at[random.randint(0, len(usernames.index)-1), 'Obj']])
                
                self.connection_established = True
                
            except socket.error as exc:
                print(f"[DEBUG]: Couldn't connect with server, \n[Error]: {exc}")
        
    
    def draw(self):
        if self.connection_established:
            for message in self.messages:
                if self.message_space.contains(message.rect):
                    message.draw(self.screen)
            self.screen.blit(self.username_surf, self.username_rect)
            pygame.draw.rect(self.screen, (230, 230, 230), self.username_box, 1, 6)
        
        else:
            self.screen.blit(self.conn_lost_surf, self.conn_lost_rect)
            self.screen.blit(self.conn_lost_text, self.clt_rect)
        
        self.screen.blit(self.beta, (self.catchat_textrect.topright[0]-20, self.catchat_textrect.topright[1]))         # Beta icon
        self.screen.blit(self.send_icon, self.send_rect)                                                               # Send Button
        self.textbox.draw(self.screen)
        
    def keydown(self, event):
        # if self.connection_established:
            if self.textbox.keydown(event):
                self.send_msg()
    
    def new_msg(self, msg, user='You'):
        if self.connection_established:
            if user == 'You':
                self.messages.append(Message(msg, self.message_space.top if len(self.messages) == 0 else self.messages[-1].rect.bottom, user=user))
            else:
                # Assign the new user a color and a username
                username = user
                if username not in self.users:
                    # Usernames are alloted randomly since kets don't need recognition (not because Garv was too lazy to implement it properly)
                    self.users[username] = r_c()
                self.messages.append(Message(msg, self.message_space.top if len(self.messages) == 0 else self.messages[-1].rect.bottom, username, self.users[username]))
            self.scroll_vel = -100
        
    def send_msg(self):
        if self.connection_established:
            self.new_msg(self.textbox.last_text)
            self.send_to_server(self.textbox.last_text)
            self.msg_send_sound.play()
        else:
            if self.textbox.last_text == '!reconnect':
                print("[CONNECTION]: Reattempting Connection to server...")
                self.attempt_connection()
    
    def send_to_server(self, msg):
        if self.connection_established:
            msg = f'{self.username}: {msg}'
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.socket.send(send_length)
            self.socket.send(message) 
            print(f'[MESSAGE]: Sent message - {message}')
            
    
    def click(self, pos):
        if self.connection_established:
            if self.send_rect.collidepoint(pos) and self.connection_established:
                self.send_msg()
    
    def recieve(self):
        self.recieve_msgs = True
        print(f'[CONNECTION]: Reciever Listening')
        while self.recieve_msgs:
            msg_length = self.socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                recieved = self.socket.recv(msg_length).decode(FORMAT).split(': ', maxsplit=1)
                username, msg = recieved
                self.new_msg(msg, username)
                print(f'[MESSAGE]{username=}: {msg=}')
                
                self.msg_recieve_sound.play() if self.focused else self.you_got_a_text.play()
            
    
    def update(self, mouse_pos, dt):
        if self.connection_established:
            if self.scroll_vel != 0 and len(self.messages) > 0:
                self.move_by((0, self.scroll_vel))
                self.scroll_vel = min(0, self.scroll_vel+self.scroll_resistance) if self.scroll_vel < 0 else max(0, self.scroll_vel-self.scroll_resistance)
                self.scroll_vel = max(-self.max_scroll_vel, self.scroll_vel) if self.scroll_vel < 0 else min(self.max_scroll_vel, self.scroll_vel)
    
    def move_by(self, increment):
        if self.connection_established:
            top_y, bottom_y = self.messages[0].rect.top, self.messages[-1].rect.bottom
            if top_y < self.message_space.top or bottom_y > self.message_space.bottom:
                del_x, del_y = increment
                
                if del_y + top_y > self.message_space.top:
                    del_y = self.message_space.top - top_y
                    self.scroll_vel = 0
                elif del_y + bottom_y < self.message_space.bottom:
                    del_y = self.message_space.bottom - bottom_y
                    self.scroll_vel = 0
                
                for msg in self.messages:
                    msg.rect.top += del_y
    
    def scroll(self, s, mouse_pos):  
        if self.connection_established:
            self.scroll_vel += s[1]*scroll_senstivity
    
    def on_focus(self):
        self.focused = True
        
    def switch_focus(self):
        self.focused = False
                
        # TODO: Catmode: Toggle that converts all text to MEOW MEOW MEOW
