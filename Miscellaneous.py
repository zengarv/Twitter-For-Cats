import pygame
import numpy as np
from math import sin, cos, radians, pi, atan2, degrees
import random
from Settings import *

class Rat:
    """
    Jerry refused to feature in this part (he was showing too much attitude)
    """
    def __init__(self, screen):
        self.surfs = [pygame.transform.smoothscale(pygame.transform.rotate(pygame.image.load(r'images\R-A-T-S\mouse.png'), 16), (120, 77)),
                      pygame.transform.smoothscale(pygame.image.load(r'images\R-A-T-S\ant.png'), (600//7, 435//7)),
                      pygame.transform.smoothscale(pygame.image.load(r'images\R-A-T-S\ladybug.png'), (482//8, 436//8)),
                      pygame.transform.smoothscale(pygame.image.load(r'images\R-A-T-S\laserdot.png').subsurface((126-22, 126-22, 44, 44)), (30, 30))]
        self.image = random.choice(self.surfs)
        
        self.screen = screen
        self.center = np.array([0, 0])  # This is center pos.
        self.v = 10
        self.vel = np.array([0, 0])
        
        self.max_angular_vel = 5
        self.exist = False
        
        self.kill()
        
    
    def draw(self):
        """
        This is what Walt Disney did (he drew stuff)
        """
        if self.exist:
            self.rotated_image = pygame.transform.rotate(self.image, (-self.angle))
            self.rot_rect = self.rotated_image.get_rect()
            self.rot_rect.center = self.center
            self.screen.blit(self.rotated_image, (self.center[0]-self.rot_rect.width//2, self.center[1]-self.rot_rect.height//2))
            # pygame.draw.rect(self.screen, (20, 240, 55), self.rot_rect, width=2)    # Hitbox
        
    def update(self, dt):
        if self.exist:
            self.angular_acceleration= (random.random()-0.5)*1.5
            
            # self.angular_acceleration += self.angular_jerk
            self.angular_speed += self.angular_acceleration
            
            if abs(self.angular_speed) > self.max_angular_vel:
                self.angular_speed = self.max_angular_vel*self.angular_speed/abs(self.angular_speed)
            
            self.angle += self.angular_speed
            
            self.vel[0] = self.v*cos(radians(self.angle))
            self.vel[1] = self.v*sin(radians(self.angle))
            self.center = self.center + self.vel

        self.t += dt

        if self.t >= 2 and not self.on_screen():
            self.kill()
        if self.t >= 0 and not self.exist:
            self.spawn()
    
    def kill(self):
        """---Redacted---"""
        self.exist = False
        self.t = -random.randint(mouse_time_ll, mouse_time_ul)
        
    def click(self, pos):
        # KLIK KLIK
        if self.exist and self.rot_rect.collidepoint(pos):
            # self.spawn()
            squish.play()
            self.kill()
            return True
    
    def on_screen(self):
        """
        I didn't need a function for this but that applies to many things in life and I still have them
        """
        return self.rot_rect.colliderect(self.screen.get_rect())
    
    def spawn(self):
        self.image = random.choice(self.surfs)
        
        self.exist = True
        self.center[0], self.center[1] = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.angle = random.randint(0, 360)
        
        self.rotated_image = pygame.transform.rotate(self.image, (-self.angle))
        self.rot_rect = self.rotated_image.get_rect()
        self.rot_rect.center = self.center
        
        self.vel[0] = self.v*cos(radians(self.angle))
        self.vel[1] = self.v*sin(radians(self.angle))
        
        while self.on_screen():
            self.center -= self.vel*10
            self.rot_rect.center = self.center
            
        self.angular_speed = (random.random()-0.5)*3
        
        
        self.t = 0


class SelfDestruct:
    """
    My homework excuse (it self destructed)
    """
    def __init__(self, screen):
        self.t = 0
        self.wait_time = 0
        
        self.count = '---'
        self.screen = screen
        self.initiated = False
        self.WIDTH, self.HEIGHT = screen.get_size()
        
        self.red_filter = pygame.surface.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.red_filter.fill((240, 40, 22))
        self.red_filter.set_alpha(50)
        
        # Osama Bin Ket
        self.cat_bomb = pygame.image.load(r"images\cat bomb.png")
        self.bombcat_size = self.cat_bomb.get_size()
        self.cat_bomb = pygame.transform.smoothscale(self.cat_bomb, (self.bombcat_size[0]//1.5, self.bombcat_size[1]//1.5))
        self.bombcat_rect = self.cat_bomb.get_rect()
        
        self.bc_bry_f = self.HEIGHT
        self.bc_bry_i = self.HEIGHT + self.bombcat_size[1]
        self.bc_brx = self.WIDTH//2 + 150
        self.bombcat_rect.bottomright = self.bc_brx, self.bc_bry_i
        self.cat_anim_duration = 1.5
        
        self.o = 10
        
        self.draw_surf()
    
    def update(self, dt):
        self.t += dt
        if self.initiated and self.t <= self.end_t: self.bombcat_rect.bottomright = self.bc_brx, max(-(sin(pi/2*(self.t-self.start_t)/(self.cat_anim_duration)))*self.bombcat_size[1] + self.bc_bry_i, self.bc_bry_f)
        
        if self.initiated and self.update_count_at <= self.t:
            if self.update_count(): return True
            else: self.update_count_at = self.t + time_between_counts
    
    def initiate_self_destruct_sequence(self):
        """ Makes thingy go Boom (eventually) """
        if not self.initiated:
            self.initiated = True
            self.start_t = self.t
            self.end_t = self.start_t + self.cat_anim_duration
            self.update_count_at = self.t + time_between_counts
            BEEP_SOUND.play()
    
    def update_count(self):
        """ Except this guy does not know how to count """
        if self.count == '0': return True
        self.count = str(random.randint(0, 10))
        self.draw_surf()
        if self.count != '0':BEEP_SOUND.play()
        else: pixel_boom.play()
    
    def draw_surf(self):
        """Do some picasso"""
        self.surf = pygame.surface.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.surf.blit(self.red_filter, (0, 0))
        
        count_down = Count_Down_font.render(self.count, True, (255, 255, 255))
        self.surf.blit(count_down, ((WIDTH - count_down.get_width())//2, (HEIGHT - count_down.get_height())//2 + count_down_height_offset))
        self_destructing_in = Count_Down_fontS.render("Self Destructing in:", True, (255, 255, 255))
        self.surf.blit(self_destructing_in, ((WIDTH - self_destructing_in.get_width())//2, (HEIGHT - count_down.get_height() - self_destructing_in.get_height() - 50)//2 + count_down_height_offset))
        
        
    def draw(self):
        """More picasso"""
        if self.initiated:
            self.o = min(255, self.o*1.075)
            self.surf.set_alpha(self.o)
            self.screen.blit(self.surf, (0, 0))

            self.screen.blit(self.cat_bomb, self.bombcat_rect)

class Paw:
    def __init__(self, paw_cursor:pygame.Surface, screen):
        self.t = 0
        self.screen = screen
        self.held = False
        self.paw_surf = paw_cursor
        self.w, self.h = paw_cursor.get_size()
        self.missiles = []
        pygame.mouse.set_cursor(pygame.Cursor((self.w//2, self.h//2), paw_cursor))
                
        self.reticle = pygame.surface.Surface((32, 32))
        # 256 x 582
        self.reticle.fill(reticle_col)
        self.mask = crosshairs[crosshair_index]
        self.reticle.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGB_MIN)
        self.reticle.set_colorkey((0, 0, 0))
    
        
    def update(self, dt, mouse_pos):
        self.x1, self.y1 = mouse_pos
        self.t += dt
        
        for missile in self.missiles:
            if missile.update(dt):
                self.missiles.remove(missile)
                del missile
            
        if self.held:
            del_x, del_y = (self.y1-self.y0), (self.x1-self.x0)
            self.a = 180+(atan2(del_y, del_x) if del_x != 0 else pi/2 if del_x > 0 else -pi/2)*180/pi
            if del_x == 0 and del_y == 0: self.a = 0
            
        self.draw()
    
    def draw(self):
        if self.held:
            self.rot_paw = pygame.transform.rotate(self.missile_head, self.a)
            self.rot_paw_rect = self.rot_paw.get_rect()
            self.rot_paw_rect.center = self.x0, self.y0
            self.screen.blit(self.rot_paw, self.rot_paw_rect)
    
        for missile in self.missiles:
            missile.draw(self.screen)
            
    def keydown(self, mouse_pos):
        ab_stretch.play()
        self.held = True
        self.missile_head = boeing if random.random() < boeing_spawn_chance else self.paw_surf         # Easter Egg: Boeing Missile System
        pygame.mouse.set_cursor(pygame.Cursor((32//2, 32//2), self.reticle))
        self.x0, self.y0 = mouse_pos
            
    def keyup(self):
        self.held = False
        pew.play()
        pygame.mouse.set_cursor(pygame.Cursor((self.w//2, self.h//2), self.paw_surf))
        self.missiles.append(Missile(self.missile_head, (self.x0, self.y0), self.a-180))

    def click(self, mouse_pos):
        pass
    
        
class Missile:
    def __init__(self, surf:pygame.Surface, pos, angle):
        self.surf = surf
        self.surf_rect = surf.get_rect()
        self.surf_rect.top = 6
        self.sx, self.sy = surf.get_size()
        
        self.px, self.py = pos
        self.angle = angle
        self.has_exploded = False
          
        self.a = 0.2
        self.ax, self.ay = self.a*sin(radians(self.angle)), self.a*cos(radians(self.angle))
        self.vx, self.vy = 0, 0
        self.flicker_rect = burner_flicker[0].get_rect()
        self.bf_w, self.bf_h = self.flicker_rect.width, self.flicker_rect.height
        self.flicker_rect.midtop = (max(self.sx/2, self.bf_w/2), self.sy)
        
        self.boom_rect = boom[0].get_rect()
        
        self.at = 0
        self.anim_time = 0.15
        self.anim_i = 0
        
        self.draw(None)
    
    def update(self, dt):
        self.at += dt
        if self.at >= self.anim_time:
            self.at = 0
            if not self.has_exploded: self.anim_i = (self.anim_i + 1) if self.anim_i != len(burner_flicker)-1 else 6
            else:
                if self.anim_i != len(boom)-1:
                    self.anim_i = (self.anim_i + 1)
                else: return True
        if not self.has_exploded:
            self.vx, self.vy = self.vx + self.ax, self.vy + self.ay
            if not (0 <= self.px+self.vx <= WIDTH and 0 <= self.py+self.vy <= HEIGHT):
                self.explode()
                return
            self.px, self.py = self.px+self.vx, self.py + self.vy
    
    def draw(self, screen):
        if not self.has_exploded:
            self.surf_with_flicker = pygame.surface.Surface((max(self.sx, self.bf_w), self.sy+self.bf_h), pygame.SRCALPHA)
            self.surf_with_flicker.blit(burner_flicker[self.anim_i], self.flicker_rect)
            self.surf_with_flicker.blit(self.surf, self.surf_rect)
            
            self.rot_surf = pygame.transform.rotate(self.surf_with_flicker, self.angle+180)
            self.rot_surf_rect = self.rot_surf.get_rect()
            self.rot_surf_rect.center = self.px, self.py
            if screen != None: screen.blit(self.rot_surf, self.rot_surf_rect)
        else:
            if screen != None: screen.blit(boom[self.anim_i], self.boom_rect)
        
    def explode(self):
        impact.play()
        self.has_exploded = True
        self.anim_i=0
        self.anim_time=0.03
        self.boom_rect.center = self.px, self.py

def add_fade(sprites, n, decay_factor = 0.75, o=255):
    s = sprites[-1]
    size = s.get_size()
    
    for i in range(n):
        o *= decay_factor
        surf = pygame.surface.Surface(size, pygame.SRCALPHA)
        s.set_alpha(o)
        surf.blit(s, (0, 0))
        sprites.append(surf)
    
    return sprites


boom = [pygame.image.load(f'images\\explosion\\{i}.png') for i in range(1, 25)]
boom = add_fade(boom, 10, decay_factor=0.7, o=150)

crosshair_sheet = SpriteSheet(r'images\crosshairs.jpg')
crosshairs = crosshair_sheet.from_sheet(512//8, 8, 8, 32)

