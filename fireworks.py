import pygame
from math import sin, cos, pi
import random

from Settings import HEIGHT, WIDTH, FPS, fireworks_color_offset

g = 500
r_c = lambda: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Particle:
    def __init__(self, pos, vel, mass, radius, color):
        self.pos = pos
        self.vel = vel   # [x, y]
        self.mass = mass
        self.radius = radius
        self.color = color
        self.age = 0

    def update(self, dt):
        self.age += dt
        self.vel[1] += g * dt
        self.radius *= 0.996
        self.pos = [self.pos[0] + self.vel[0] * dt, self.pos[1] + self.vel[1] * dt]
        
        if not (0 <= self.pos[0] <= WIDTH and 0 <= self.pos[1] <= HEIGHT):
            return True
        return False
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Firework:
    # Fireworks go BOOM BOOM
    def __init__(self, x, vel, color, screen, mass=10, max_age=3, y=HEIGHT):
        self.pos = [x, y]
        self.vel = vel
        self.color = color
        self.exploded = False
        self.max_age = max_age
        self.mass = mass
        
        self.particles = []
        self.trail = []
        self.max_p_vel = 250
        
        self.decay_factor = 0.7
        self.last_frame = pygame.surface.Surface(screen.get_size(), pygame.SRCALPHA)
        self.last_frame.set_alpha(255*self.decay_factor)
        self.screen = screen
        
        self.dimens = [random.randint(20, 80)/10, random.randint(50, 150)/10]
        
    def explode(self):
        # This is what happened to the plane on 9/11 (it explode)
        self.exploded = True
        num_particles = random.randint(50, 200)
        for _ in range(num_particles):
            theta = random.random()*2*pi
            x, y = random.random(), random.random()
            vel = [self.max_p_vel * cos(theta) * x, self.max_p_vel * sin(theta)*y]
            self.particles.append(Particle(self.pos, vel, random.uniform(1, 5), random.randint(10, 50)/10, offsetted_color(self.color)))
    
    def draw(self):
        # This did not happen during 9/11
        firework_screen = pygame.surface.Surface((self.screen.get_size()), pygame.SRCALPHA)
        if not self.exploded:
            pygame.draw.rect(firework_screen, self.color, (self.pos[0]-self.dimens[0]/2, self.pos[1]-self.dimens[1]/2, self.dimens[0], self.dimens[1]))
            for p in self.trail:
                p.draw(firework_screen)
        else:
            for p in self.particles:
                p.draw(firework_screen)
        
        firework_screen.blit(self.last_frame, (0, 0))
        self.screen.blit(firework_screen, (0, 0))
        self.last_frame = firework_screen
        self.last_frame.set_alpha(255*self.decay_factor)

    def update(self, dt):
        # Make the particles fall (This is what happened to the towers during 9/11)
        if not self.exploded:
            self.vel[1] += g * dt
            self.pos = [self.pos[0] + self.vel[0] * dt, self.pos[1] + self.vel[1] * dt]
            if self.vel[1] >= 0: 
                self.explode()
            if random.randint(1, int(FPS/40))==1:
                self.trail.append(Particle(self.pos, [random.randint(-40, 40), 0], self.mass, random.randint(5, 30)/10, offsetted_color(self.color)))
            for t in self.trail:
                t.update(dt)
                if t.age > self.max_age or t.radius < 0.2:
                    self.trail.remove(t)
            
        else:
            for p in self.particles: 
                outside_screen = p.update(dt)
                if p.age > self.max_age or p.radius < 0.5 or outside_screen:
                    self.particles.remove(p)

def offsetted_color(color):
    # Generate a random color that is slightly different from the given color
    r = random.randint(max(color[0] - fireworks_color_offset, 0), min(color[0] + fireworks_color_offset, 255))
    g = random.randint(max(color[1] - fireworks_color_offset, 0), min(color[1] + fireworks_color_offset, 255))
    b = random.randint(max(color[2] - fireworks_color_offset, 0), min(color[2] + fireworks_color_offset, 255))
    return (r, g, b)
