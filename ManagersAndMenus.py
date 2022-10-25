import os
import random
from math import pi, sin

import pandas as pd
import pygame

from Settings import *
import threading

pygame.init()

def load_screen(screen, font):
    # Make the load stuff part look good
    screen.fill(tweet_bg_col)
    GRUMPS.convert_alpha()
    screen.blit(GRUMPS, ((- GRUMPS.get_width() + WIDTH)//2, (- GRUMPS.get_height() + HEIGHT)//2))
    pygame.display.update()
    loading = font.render("Loading...", True, (255, 255, 255))
    screen.blit(loading, ((WIDTH-loading.get_width())//2, (HEIGHT-loading.get_height()+GRUMPS.get_height())//2 + 30))
    pygame.display.update()


# cat_crossbones = pygame.transform.smoothscale(pygame.image.load(r'images\catcrossbones.png').convert_alpha(), (40, 40))
cat_button_raised = pygame.transform.smoothscale(pygame.image.load(r'images\cat crossbones\catcrossbones raised.png').convert_alpha(), (50, 50))
cat_button_pressed = pygame.transform.smoothscale(pygame.image.load(r'images\cat crossbones\catcrossbones pressed.png').convert_alpha(), (50, 50))
cat_crossbones = cat_button_raised

def render_fixwidth_text(text, font, width, col=(255, 255, 255), linespace = 10):
    text = text.replace('\t', '    ')
    # It does pretty much what it says (it renders text)
    text_surfaces = []
    line = ''
    
    for word in text.split():
        if font.size(line + ' ' + word)[0] <= width:
            line = line + ' ' + word
        
        else:
            text_surfaces.append(font.render(line.strip(), True, col))
            line = word
    text_surfaces.append(font.render(line.strip(), True, col))
    
    
    h = [i.get_height() for i in text_surfaces]
    textSurf = pygame.surface.Surface((width, (len(text_surfaces)-1)*linespace + sum(h)), pygame.SRCALPHA)
    
    y = 0
    for t in text_surfaces:
        textSurf.blit(t, (0, y))
        y += t.get_height() + linespace
    
    return textSurf

class Tweet:
    """
    When I first wrote this only god and I understood it. Now only god does.
    """
    # mask = pygame.surface.Surface((pfp_s, pfp_s))
    # mask.fill((0, 0, 0))
    # pygame.draw.circle(mask, (255, 255, 255), (pfp_s//2, pfp_s//2), pfp_s//2)
    
    mask = pygame.image.load(r'images\misc\pfp mask.png')
    gloss = pygame.image.load(r'images\misc\gloss white.png')
    gloss.set_alpha(25)
    
    
    def __init__(self, pos, width=WIDTH):
        self.pos = pos
        self.alpha = 255
        self.width = width
        self.tweettext = tweets.at[random.randint(0, len(tweets.index)-1), 0]
        self.hand = random.choice([usernames.at[random.randint(0, len(usernames.index)-1), 'Handles'], usernames.at[random.randint(0, len(usernames.index)-1), 'Adj'] + usernames.at[random.randint(0, len(usernames.index)-1), 'Obj']])
        
        self.username_surf = username_font.render(self.hand, True, username_text_col)
        self.handle_surf = handlefont.render('@' + self.hand, True, handle_text_col)
        self.tweet_text_surf = render_fixwidth_text(self.tweettext, tweetfont, width-150, col=tweet_text_col, linespace=tweet_linespace)
        
        self.pfp_surf = random.choice(cat_imgs)
        self.pfp_surf = pygame.transform.smoothscale(self.pfp_surf, (pfp_s, pfp_s))
        
        self.pfp_surf.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.pfp_surf.set_colorkey((0, 0, 0))
        
        self.height = 20+pfp_s+self.tweet_text_surf.get_height()
        self.surf = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill(tweet_bg_col)
        
        self.surf.blit(pygame.transform.smoothscale(self.gloss, (self.width, self.height)), (0, 0))
        
        self.surf.blit(self.tweet_text_surf, (username_pos[0], username_pos[1]+5+self.username_surf.get_height()))
        self.surf.blit(self.pfp_surf, pfp_pos)
        
        self.surf.blit(self.username_surf, username_pos)
        self.surf.blit(self.handle_surf, (username_pos[0] + self.username_surf.get_width() + 5, username_pos[1]))
        self.rect = pygame.rect.Rect(*self.pos, self.width, self.height)
        self.disintegrated = False
        
        pygame.draw.rect(self.surf, ACCENT_COL, (0, 0, self.width, self.height), width=1, border_radius=tweet_roundedcorner_radius)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
    
    def disappear(self, strength):
        """
        Majik
        """
        self.alpha *= strength
        self.surf.set_alpha(self.alpha)
    
    def move(self, new_pos):
        """
        https://youtu.be/ApuFuuCJc3s?t=31
        """
        self.pos = new_pos
        self.rect = pygame.rect.Rect(*self.pos, self.width, self.height)
    
    def move_by(self, increment):
        del_x, del_y = increment
        self.move((self.pos[0] + del_x, self.pos[1] + del_y))


class BurgerMenu:
    glass = pygame.image.load(r'images\misc\glass.png')
    glass.set_alpha(50)
    """
    https://youtu.be/TSSPDoXIPEU?t=5
    """
    def __init__(self, screen, menus):
        self.t = 0
        self.collapsed = True
        self.menus, self.menu_names = [], []
        self.icons = []
        self.menu_button_surf = []
        self.menu_button_rects = []
        
        for m in menus:
            self.menus.append(m[0])
            self.menu_names.append(m[1])
            self.icons.append(pygame.transform.smoothscale(pygame.image.load(m[2]), (50, 50)))
        
        self.screen = screen
        # self.burger_surf = pygame.transform.smoothscale(pygame.image.load(r'images\burger.png'), (40, 40))
        self.burger_index = 0
        self.burger_frametime = 0.045
        self.burger_next = -1
        self.burger_rect = burger[0].get_rect()
        self.burger_rect.topleft = (0, 0)
        
        self.width = 300
        self.menu_surf = pygame.Surface((self.width, HEIGHT))
        self.menu_rect = self.menu_surf.get_rect()
        self.menu_rect.right = 0
        
        self.selected_menu_index = 0
        self.selected_menu = self.menus[self.selected_menu_index]
        self.menu_buttons_top = 200
        self.menu_button_height = 80
        self.draw_surf()

        self.slide_duration = 0.3
        self.slide_start = 0
        self.slide_end = 0
        
        self.strikethrough_surf = pygame.transform.smoothscale(pygame.image.load(r'images\strikethrough.png'), (1773//10.5, 245//10.5))
        self.strikethrough_rect = self.strikethrough_surf.get_rect()
        self.strikethrough_rect.center = 225, 45

        
    def draw(self):
        self.selected_menu.draw()
        
        if self.selected_menu_index != 0:
            self.screen.blit(self.strikethrough_surf, self.strikethrough_rect)
            self.screen.blit(self.title_textsurf, self.title_textrect)
            
        if self.slide_end >= self.t or not self.collapsed: 
            self.screen.blit(self.menu_surf, self.menu_rect)
        
        self.screen.blit(burger[self.burger_index], self.burger_rect)
    
    def draw_surf(self):
        self.menu_surf.fill((15, 15, 15))
        self.menu_button_surf.clear()
        
        y = self.menu_buttons_top
        for names, icons in zip(self.menu_names, self.icons): 
            
            menu_button_surf = pygame.Surface((self.width, self.menu_button_height), pygame.SRCALPHA)
            menu_button_surf.blit(pygame.transform.smoothscale(self.glass, (self.width, self.menu_button_height)), (0, 0))
            menu_button_rect = menu_button_surf.get_rect()
            
            name_surf = burger_menu_font.render(names, True, burger_menu_text_col)
            name_rect = name_surf.get_rect()
            name_rect.midleft = (90, menu_button_rect.centery)
            
            menu_button_surf.blit(name_surf, name_rect)
            menu_button_rect.top = y
            self.menu_surf.blit(menu_button_surf, menu_button_rect)
            
            icon_rect = icons.get_rect()
            icon_rect.midleft = (20, menu_button_rect.centery)
            self.menu_surf.blit(icons, icon_rect)
            
            pygame.draw.line(self.menu_surf, ACCENT_COL, (menu_button_rect.left + 20, menu_button_rect.top), (menu_button_rect.right - 20, menu_button_rect.top))
            pygame.draw.line(self.menu_surf, ACCENT_COL, (menu_button_rect.left + 20, menu_button_rect.bottom), (menu_button_rect.right - 20, menu_button_rect.bottom))
            
            y += self.menu_button_height
            
            self.menu_button_surf.append(menu_button_surf)
            self.menu_button_rects.append(menu_button_rect)
        
        self.menu_surf.set_alpha(220)
        
        
    def click(self, mouse_pos):
        if self.burger_rect.collidepoint(mouse_pos):             # If burger is clicked
            self.burger_next = self.t + self.burger_frametime
            self.collapse()
            return
        
        if self.collapsed:                          # Update the active menu if burger menu is not active
            self.selected_menu.click(mouse_pos)
        
        if self.menu_rect.collidepoint(mouse_pos):
            for i, (menu, rect) in enumerate(zip(self.menus, self.menu_button_rects)):
                if rect.collidepoint(mouse_pos):
                    self.selected_menu_index = i
                    self.selected_menu.switch_focus()
                    
                    self.title_textsurf = pygame.font.Font('fonts\\pico.ttf', 40).render(self.menu_names[self.selected_menu_index], True, ((54, 151, 255)))
                    self.title_textrect = self.title_textsurf.get_rect()
                    self.title_textrect.center = 225, 78
                    
                    self.selected_menu = menu
                    self.selected_menu.on_focus()
                    self.collapse()
                    break
        elif not self.collapsed: self.collapse()            # Close the menu if it's not clicked on
                
    def mouse_button_up(self, event):
        self.selected_menu.mouse_button_up(event)
        
    def mouse_button_down(self, event):
        self.selected_menu.mouse_button_down(event)
    
    def collapse(self):
        self.collapsed = not self.collapsed
        self.slide_start = self.t
        self.slide_end = self.t + self.slide_duration
            
    def update(self, dt, mouse_pos):
        self.t += dt
        self.selected_menu.update(mouse_pos, dt)
        
        if self.slide_end >= self.t:
            if not self.collapsed: 
                self.menu_rect.right = self.width-sin(pi/2*(self.slide_end-self.t)/self.slide_duration)*self.width
            else: 
                self.menu_rect.right = sin(pi/2*(self.slide_end-self.t)/self.slide_duration)*self.width
        else:
            self.menu_rect.right = self.width if not self.collapsed else 0
        
        if self.burger_next <= self.t and self.burger_next != -1:
            self.burger_index += 1
            if self.burger_index == len(burger):    
                self.burger_next = -1
                self.burger_index = 0
            else: self.burger_next = self.t + self.burger_frametime
    
    def hover(self, pos):
        self.selected_menu.hover(pos)
    
    def scroll(self, event, mouse_pos):
        self.selected_menu.scroll(event, mouse_pos)
    
    def keydown(self, event):
        self.selected_menu.keydown(event)
    
    def keyup(self, event):
        self.selected_menu.keyup(event)
    
class BMBuilder:
    def __init__(self, screen, pos):
        self.pos = pos
        self.screen = screen
                
    def draw(self):
        pass
        
    def click(self, pos):
        pass
    
    def mouse_button_up(self, event):
        pass
    
    def mouse_button_down(self, event):
        pass
    
    def keydown(self, event):
        pass
    
    def keyup(self, event):
        pass
    
    def update(self, mouse_pos, dt):
        pass
    
    def hover(self, pos):
        pass

    def scroll(self, event, pos):
        pass

    def switch_focus(self):
        pass
    
    def on_focus(self):
        pass

class TweetManager(BMBuilder):
    """
    Passionate Manager and CSE with 4+ years of experience, seeking position with Carlon Stoves. Grew buisness by 15% per year.
    Proceeded to use all the company revenue, then get fired. Need job asap
    """
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.topleft = pos
        self.x, self.y = pos
        self.tweets = []
        self.visible_tweets = []
        self.invalidated_opinions = []
        self.width = WIDTH - pos[0]
        self.surf = pygame.surface.Surface((WIDTH-pos[0], HEIGHT-pos[1]))
        self.generate_tweets()
        
        self.top_i = 0
        self.bottom_i = len(self.tweets)-1
        self.active_tweet = None
        
        self.scroll_vel = 0
        self.scroll_resistance = 1           # Lower for smoother scrolling, higher for better performance
        self.max_scroll_vel = 20
        
        self.t = 0
        
        self.cathand_start_t = -1
        self.cathand_end_t = -1
        self.cathand_anim_dur = 2.5
        self.cathand_surf = pygame.image.load(r'images\cathand.png')
        size = self.cathand_surf.get_size()
        scaling_factor=1.8
        self.cathand_surf = pygame.transform.smoothscale(self.cathand_surf, (size[0]/scaling_factor, size[1]/scaling_factor))
        self.cathand_rect = self.cathand_surf.get_rect()
        self.cathand_rect.midright = 0, 870  #  Final x: 600
        
        self.cat_button_rect = pygame.rect.Rect(0, 0, 40, 40)
        self.tweet_button_surf = pygame.transform.smoothscale(pygame.image.load(r'images\icons\tweetbutton.png'), (60, 60))
        self.tweet_button_rect = self.tweet_button_surf.get_rect()
        self.tweet_button_rect.center = WIDTH - 60, HEIGHT - 60
        self.tweet_button_visible = True
        self.tweet_button_clicked = False
        
        self.held_tweets = [Tweet((0, 0), self.width) for _ in range(5)]
        self.held_tweets_generating = False
        
        self.draw_surf()
        
    def draw(self):
        self.screen.blit(self.surf, self.topleft)
        
        if self.tweet_button_visible: self.screen.blit(self.tweet_button_surf, self.tweet_button_rect)
        if self.tweet_button_clicked:self.screen.blit(self.cathand_surf, self.cathand_rect)
        
    
    def draw_surf(self):
        
        self.surf.fill(tweet_bg_col)
        for tweet in self.visible_tweets: 
            tweet.draw(self.surf)
        
        if self.active_tweet is not None:
            pygame.draw.rect(self.surf, HIGHLIGHT_COL, self.active_tweet.rect, 1, tweet_roundedcorner_radius)    # Active Tweet Rectangle
            mr = self.active_tweet.rect.midright
            self.cat_button_rect.midright = mr[0] - 20, mr[1]
            
            self.surf.blit(cat_crossbones, self.cat_button_rect)
                        
    def update(self, mouse_pos, dt):
        self.t += dt
        for tweet in self.invalidated_opinions:
            tweet.disappear(0.99)
            if tweet.alpha < 0.01:
                self.invalidated_opinions.remove(tweet)
                tweet.surf = pygame.surface.Surface(tweet.surf.get_size())
                tweet.surf.fill(tweet_bg_col)
        
        if not self.held_tweets_generating and len(self.held_tweets) < 5:
            self.generate_tweets_thread = threading.Thread(target=self.update_held_tweets)
            self.generate_tweets_thread.start()
                
        if self.scroll_vel != 0:
            self.move_by((0, self.scroll_vel))
            self.hover(mouse_pos)
            self.scroll_vel = min(0, self.scroll_vel+self.scroll_resistance) if self.scroll_vel < 0 else max(0, self.scroll_vel-self.scroll_resistance)
            self.scroll_vel = max(-self.max_scroll_vel, self.scroll_vel) if self.scroll_vel < 0 else min(self.max_scroll_vel, self.scroll_vel)
            
        if len(self.invalidated_opinions) > 0: 
            self.draw_surf()
        
        if self.tweet_button_clicked and self.tweet_button_visible:
            p = (self.cathand_end_t-self.t)
            self.cathand_rect.right = 600*sin(pi*(p/(self.cathand_anim_dur)))
            if self.t > self.cathand_start_t + self.cathand_anim_dur/2:
                self.tweet_button_rect.centerx = WIDTH - 60 - self.topleft[0] - (600 - self.cathand_rect.right)

            
            if p < 0: self.tweet_button_visible = False
    
    def update_held_tweets(self):
        self.held_tweets_generating = True
        while len(self.held_tweets) < 5:
            self.held_tweets.append(Tweet((0, 0), self.width))
        self.held_tweets_generating = False
        
    
    def generate_tweets(self):
        x, y = self.x, self.y
        while y < HEIGHT-self.topleft[1]+(self.visible_tweets[-1].rect.height if len(self.visible_tweets) else 0):
            t = Tweet((0, y-self.topleft[1]), width=self.width)
            self.tweets.append(t)
            self.visible_tweets.append(t)
            y += self.tweets[-1].surf.get_height()
        
    def move(self, new_pos):
        x0, y0 = self.x, self.y
        self.x, self.y = new_pos
        del_x, del_y = self.x-x0, self.y-y0
        
        self.visible_tweets.clear()
        for tweet in self.tweets:
            tweet.move_by((del_x, del_y))
            top = tweet.pos[1]
            bottom = tweet.pos[1] + tweet.height           
            if not ((top > HEIGHT and bottom > HEIGHT) or (top < 0 and bottom < 0)):   
                self.visible_tweets.append(tweet)
                
        self.draw_surf()
        
    def move_by(self, increment):
        del_x, del_y = increment
        
        top_y = self.tweets[0].pos[1]      
        if top_y + del_y >= 0:
            del_y = - top_y
        
        bottom_y = self.tweets[-1].pos[1] + self.tweets[-1].height
        if HEIGHT + 100 > bottom_y:
            tweet = self.held_tweets.pop()
            tweet.move_by((0, bottom_y))
            self.tweets.append(tweet)
        
        self.move((self.x + del_x, self.y + del_y))
    
    def hover(self, mouse_pos):
        mouse_pos = mouse_pos[0]-self.topleft[0], mouse_pos[1]-self.topleft[1]
        if self.active_tweet:
            if not self.active_tweet.rect.collidepoint(mouse_pos):
                self.active_tweet = None
                self.draw_surf()
        
        if self.active_tweet == None:
            for tweet in self.visible_tweets:
                if not tweet.disintegrated and tweet.rect.collidepoint(mouse_pos):
                    self.active_tweet = tweet
                    self.draw_surf()
    
    def click(self, mouse_pos):
        # Checking of position where rectangles are drawn wrt screen
        if self.tweet_button_visible and self.tweet_button_rect.collidepoint(mouse_pos):
            self.tweet_button_clicked = True
            self.cathand_start_t = self.t
            self.cathand_end_t = self.t + self.cathand_anim_dur
        
        # Mouse pos is relative to surface of manager
        elif self.active_tweet and self.cat_button_rect.collidepoint(mouse_pos[0] - self.topleft[0], mouse_pos[1] - self.topleft[1]):
            g_meow.play()
            cat_crossbones = cat_button_pressed
            self.active_tweet.disintegrated = True
            self.active_tweet.surf.blit(cat_crossbones, (self.cat_button_rect[0]-(self.active_tweet.pos[0]), self.cat_button_rect[1]-(self.active_tweet.pos[1])))
            self.invalidated_opinions.append(self.active_tweet)
            self.active_tweet = None
            
    
    def scroll(self, s, mouse_pos):  
        self.scroll_vel += s[1]*scroll_senstivity
