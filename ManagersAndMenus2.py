import pygame, random
from Settings import *
import os
from math import sin, pi, cos
pygame.init()
from ManagersAndMenus import render_fixwidth_text, BMBuilder

# Add going up rects (as long as key is held)
class PianoKey:
    def __init__(self, type, pos, key, topleft):
        self.topleft = topleft
        self.type = type
        self.is_keydown = False
        if type == "white":
            self.width = 50
            self.height = 220
        elif type == 'black':
            self.width = 35
            self.height = 120
        
        self.sound = mixer.Sound(f'sounds\\cat piano\\{key}.wav')
        self.rect = pygame.Rect(*pos, self.width, self.height)
        
        self.keyup_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.keyup_surf, ((200, 200, 200) if type == 'white' else (10, 10, 10)), (0, 0, self.width, self.height), border_radius=8 if type == 'white' else 5)
        pygame.draw.rect(self.keyup_surf, ((255, 255, 255) if type == 'white' else (40, 40, 40)), (0, 0, self.width, self.height-15), border_radius=8 if type == 'white' else 5)
        
        self.keydown_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.keydown_surf, ((255, 255, 255) if type == 'white' else (40, 40, 40)), (0, 0, self.width, self.height), border_radius=8 if type == 'white' else 5)
        
        self.tiles = []
        self.tile_vel = 2
        
    def draw(self, screen):
        screen.blit(self.keydown_surf if self.is_keydown else self.keyup_surf, self.rect)
    
    def keydown(self):
        self.sound.play()
        self.is_keydown = True
        self.tiles.append(pygame.Rect(0, 0, self.width-6, self.tile_vel))
        self.tiles[-1].midbottom = self.rect.midtop[0], self.rect.midtop[1] - 25
        
    def keyup(self):
        self.is_keydown = False
        self.sound.stop()
    
    def update(self):
        if self.is_keydown:
            self.tiles[-1] = self.tiles[-1].inflate((0, self.tile_vel))
            self.tiles[-1].top += self.tile_vel/2
            
        for i, tile in enumerate(self.tiles):
            tile.top -= self.tile_vel
            
            if tile.top < self.topleft[1]:
                self.tiles[i] = self.tiles[i].inflate((0, -self.tile_vel))
                self.tiles[i].top += self.tile_vel/2
                
            if tile.bottom < self.topleft[1]:
                self.tiles.pop(i)
    
class Piano(BMBuilder):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.topleft = 58, 400

        self.keys = []
        self.pressed_key = None
        
        self.cat_headphones = pygame.image.load(r'sounds\cat piano\catheadphones.png')
        self.ch_rect = self.cat_headphones.get_rect()
        self.cat_headphones = pygame.transform.smoothscale(self.cat_headphones, (self.ch_rect.width//3, self.ch_rect.height//3))
        self.ch_rect = self.cat_headphones.get_rect()
        self.ch_rect.midbottom = WIDTH//2, HEIGHT
        
        self.instructions = pygame.transform.smoothscale(pygame.image.load(r'images\catpiano guide2.png'), (862*0.58, 548*0.58))
        self.i_rect = self.instructions.get_rect()
        self.i_rect.center = WIDTH/2, 510
        
        self.show_help = False
        self.help_text = render_fixwidth_text("Press the corresponding keys on your keyboard for easier control", pygame.font.SysFont('Courier New', 18), 500, (255, 255, 255))
        self.help_text_rect = self.help_text.get_rect()
        self.help_text_rect.center = WIDTH/2, 720
        self.qm = pygame.transform.smoothscale(pygame.image.load(r'images\icons\question mark.png'), (25, 25))
        self.qm_rect = self.qm.get_rect()
        self.qm_rect.center = 50, 350
        
        black_keys_present = [1, 1, 0, 1, 1, 1, 0, 1, 1]
        
        # Fanci Math
        x = self.topleft[0]
        y = self.topleft[1]
        for k in ['C1', 'D1', 'E1', 'F1', 'G1', 'A2', 'B2', 'C2', 'D2', 'E2']:
            self.keys.append(PianoKey('white', (x, y), k, self.pos))
            x += 1
            x += 50
        x = 55 + 25 + 10
        black_keys = ['D2#', 'C2#', 'A2#', 'G1#', 'F1#', 'D1#', 'C1#']
        for i, r in enumerate(black_keys_present):
            if r: 
                self.keys.append(PianoKey('black', (x, y), black_keys.pop(), self.pos))
            x += 51
            
        #               |<----------------White Key Binds------------->|  |<---------Black Key Binds------->|
        self.keybinds = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'w', 'e', 't', 'y', 'u', 'o', 'p']
                
                
    def draw(self):
        pygame.draw.rect(self.screen, (190, 100, 100), (self.topleft[0]-25, self.topleft[1]-10, 510+50, 230+40), border_radius=20)
        pygame.draw.rect(self.screen, (230, 140, 140), (self.topleft[0]-25, self.topleft[1]-10, 510+50, 230+20), border_radius=20)
        
        for k in self.keys: 
            for tile in k.tiles:
                pygame.draw.rect(self.screen, (140, 240, 140) if k.type == 'white' else (80, 180, 80), tile, border_radius=10)
            k.draw(self.screen)

        if self.show_help: 
            self.screen.blit(self.instructions, self.i_rect)
            self.screen.blit(self.help_text, self.help_text_rect)
            
        self.screen.blit(self.qm, self.qm_rect)

        
        self.screen.blit(self.cat_headphones, self.ch_rect)
        
    def click(self, pos):
        if self.qm_rect.collidepoint(pos):
            self.show_help = not self.show_help
            return
        
        for key in self.keys[::-1]:
            if key.rect.collidepoint(pos):
                key.keydown()
                self.pressed_key = key
                break
    
    def mouse_button_up(self, pos):
        if self.pressed_key != None:
            self.pressed_key.keyup()
            self.pressed_key = None
    
    def keydown(self, event):
        if event.unicode in self.keybinds: self.keys[self.keybinds.index(event.unicode)].keydown()
    
    def keyup(self, event):
        if event.unicode in self.keybinds: self.keys[self.keybinds.index(event.unicode)].keyup()
    
    def update(self, mouse_pos, dt):
        for k in self.keys:
            k.update()


cat_sprites = [[[pygame.image.load(f'images\\cat\\{f}\\{i}') for i in os.listdir(f'images\\cat\\{f}')][j*3:(j+1)*3] for j in range(4)] for f in range(1, 17)]
for cat in cat_sprites:               # 16 cats
    for anim in cat:                  # 4 animations - down, left, right, up
        anim.append(anim[1])          # Add transition animation

class Cat:
    def __init__(self, screen, pos):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.anims = random.choice(cat_sprites)
        self.rect = self.anims[0][0].get_rect()
        self.rect.center = pos
        self.d = False
        
        self.facing = random.randint(0, 3)
        self.anim_index = 0
        self.anim_time = 0.15
        self.t = 0
        self.next_t = self.anim_time
        
        self.v = 3
        self.o = 0
        self.o_vel = 4
        
        random.choice(meows).play()
        
    def draw(self):
        self.surf = self.anims[self.facing][self.anim_index]
        if self.surf.get_alpha() != self.o:
            self.surf.set_alpha(self.o)
        self.screen.blit(self.surf, self.rect)
    
    def animate(self):
        self.anim_index += 1
        if self.anim_index == 4:
            self.anim_index = 0
        
    def update(self, dt):
        self.t += dt
        
        if self.o < 255 and not self.d:
            self.o = min(self.o+self.o_vel, 255)
        elif self.o > 0 and self.d:
            self.o = max(self.o-self.o_vel, 0)
        
        if self.next_t <= self.t:
            if not self.screen_rect.contains(self.rect):
                self.flip()
            self.next_t = self.t + self.anim_time
            self.animate()
            self.move()
    
    def kill(self):
        self.d = True
    
    # If it was hard to write, it should be hard to read
    def move(self):
        match self.facing:
            case 0: self.rect.centery += self.v
            case 1: self.rect.centerx -= self.v
            case 2: self.rect.centerx += self.v
            case 3: self.rect.centery -= self.v

    def flip(self):
        match self.facing:
            case 0: self.facing = 3
            case 1: self.facing = 2
            case 2: self.facing = 1
            case 3: self.facing = 0

class CountCats(BMBuilder):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        
        self.t = 0
        self.next_cat_t = 5
        self.next_t = self.next_cat_t
        
        self.count = 0
        self.draw_count_surf()
        
        self.target = 100
        self.aloosuit_rect = aloosuit.get_rect()
        self.aloosuit_rect.midbottom = WIDTH/2, HEIGHT + self.aloosuit_rect.height
        self.t_100 = -1
        self.anim_time = 1
        
        self.cats = []
        self.AAAAAAAAAGH = mixer.Sound(r'sounds\auuughhhhh.wav')
        self.bgm = mixer.Sound(r'sounds\bgm.wav')
        self.bgm.set_volume(0.5)
        self.playing = False
        
        self.reset_surf = pygame.transform.smoothscale(pygame.image.load(r'images\icons\reset.png'), (40, 40))
        self.reset_rect = self.reset_surf.get_rect()
        self.reset_rect.topright = WIDTH - 20, pos[1] + 20
        
        self.is_resetting = False
        self.time_until_reset = 1
        self.reset_in = self.time_until_reset

    def reset(self):
        self.bgm.fadeout(500)
        self.AAAAAAAAAGH.fadeout(500)
        self.count = 0
        self.draw_count_surf()
        self.t_100 = -1
        self.cats = []
        self.playing = False
        self.reset_in = self.time_until_reset
        self.is_resetting = False
        aloosuit.set_alpha(255)
        
    def draw_count_surf(self):
        self.font =  pygame.font.Font('fonts\\Joynoted.ttf', 120)
        self.count_surf = self.font.render(str(self.count), True, (HIGHLIGHT_COL))
        self.count_surf.set_alpha(180)
        self.count_rect = self.count_surf.get_rect()
        self.count_rect.center = self.screen.get_rect().center
    
    def spawn_cat(self, pos):
        if self.count < self.target:
            x, y = pos
            if not 24 < x < WIDTH - 24:
                if x < 24: x = 24
                else: x = WIDTH - 24
            if not 24 < y < HEIGHT - 24:
                if y < 24: y = 24
                else: y = WIDTH - 24
            self.count += 1
            self.next_t = self.t + self.next_cat_t
            
            if self.count == self.target: 
                self.playing = False
                self.bgm.fadeout(500)
                self.AAAAAAAAAGH.play()
                self.t_100 = self.t
                
            self.cats.append(Cat(self.screen, (x, y)))
            self.draw_count_surf()
                
    def draw(self):
        for cat in self.cats: cat.draw()
        self.screen.blit(self.count_surf, self.count_rect)
        
        if self.count == self.target:
            if self.is_resetting:
                aloosuit.set_alpha((self.reset_in/self.time_until_reset)*255)
            self.screen.blit(aloosuit, self.aloosuit_rect)
        
        if not self.is_resetting:
            self.screen.blit(self.reset_surf, self.reset_rect)
        else:
            # rotated_surf = pygame.transform.rotate(self.reset_surf, self.reset_in*360*2/self.time_until_reset)
            rotated_surf = pygame.transform.rotate(self.reset_surf, 30*sin(2*pi*5*(self.reset_in/self.time_until_reset)**1.8))#self.reset_in*360*2/self.time_until_reset)
            rot_rect = rotated_surf.get_rect()
            rot_rect.center = self.reset_rect.center
            self.screen.blit(rotated_surf, rot_rect)
        
    def click(self, pos):
        if self.reset_rect.collidepoint(pos): 
            self.is_resetting = True
            for cat in self.cats: cat.kill()
        elif not self.is_resetting: 
            self.spawn_cat(pos)

    def switch_focus(self):
        self.bgm.stop()
    
    def on_focus(self):
        if self.count < self.target: self.bgm.play(loops=-1)

    def update(self, mouse_pos, dt):
        self.t += dt
        
        if not self.is_resetting:
            if self.count == self.target:
                if self.t_100+self.anim_time >= self.t: self.aloosuit_rect.bottom = cos(pi/2*(self.t - self.t_100)/self.anim_time)*self.aloosuit_rect.height + HEIGHT
            
            else:
                if not self.playing:
                    self.playing = True
                    self.bgm.play(loops=-1)
                
                if self.next_t < self.t:
                    self.spawn_cat((random.randint(24, WIDTH-24), random.randint(24, HEIGHT-24)))
                    
            for cat in self.cats: cat.update(dt)

        else:
            self.reset_in -= dt
            for cat in self.cats: cat.update(dt)
            if self.reset_in < 0:
                self.reset()
            