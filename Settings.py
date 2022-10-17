from pygame import mixer
import pygame
pygame.init()
from BorrowedFromLeInternet import SpriteSheet


# User Settings

# Performance
WIDTH, HEIGHT = 625, 1000
FPS = 60   

enable_fireworks = True       # Disable to increase Performance

show_FPS = True
fps_font = pygame.font.SysFont('Courier New', 20)



# Customization
crosshair_index = 8
reticle_col = (240, 54, 23)



# Controls
scroll_senstivity = 10                       # 1: Left Mouse Click   
invalidate_opinion_button = 2                # 2: Mouse Middle Click  
firework_button = 1                          # 3: Right Mouse Click      
fireworks_color_offset = 50

# Mouse Spawn
mouse_time_ll = 5
mouse_time_ul = 10   # In seconds

# Self Destruct 
BEEP_SOUND = mixer.Sound(r"sounds\beep.mp3")
g_meow = mixer.Sound(r"sounds\g_meow.mp3")
pixel_boom = mixer.Sound(r"Sounds\pixel boom.wav")
squish = mixer.Sound(r"sounds\squish.wav")

paw_cursor = pygame.image.load(r"images\paw cream.png")
burner_flicker = [pygame.transform.smoothscale(pygame.image.load(f"images\\burner\\grow\\{i}.png"), (25, 58)) for i in range(1, 7)]
burner_flicker.extend([pygame.transform.smoothscale(pygame.image.load(f"images\\burner\\flicker\\{i}.png"), (25, 58)) for i in range(1, 7)])

logo = pygame.image.load(r'images\icons\twitterforcats.png')
impact = mixer.Sound(r'sounds\impact.wav')
pew = mixer.Sound(r'sounds\Pew.wav')
ab_stretch = mixer.Sound(r'sounds\angry birds slingshot stretch.wav')
meows = [mixer.Sound(f'sounds\\meows\\m{i}.wav') for i in range(1, 9)]

burger_menu_font = pygame.font.Font('fonts\\Joynoted.ttf', 30)
burger_menu_text_col = (240, 200, 100)
burger = [pygame.transform.smoothscale(pygame.image.load(f"images\\burger\\{i}.png"), (80, 80)) for i in range(1, 13)]

BOMB = pygame.image.load(r"images\bomb.png")
GRUMPS = pygame.transform.smoothscale(pygame.image.load(r"cats\grumps.png"), (100, 100))
boeing = pygame.transform.smoothscale(pygame.image.load(r'images\boeing.png'), (50, 50))
boeing_spawn_chance = 0.01      #  Default: 0.01

aloosuit = pygame.transform.smoothscale(pygame.image.load(r'images\aloosuit.png'), (675//3, 1322//3))

fade_in_factor = 1.1    # Default: 1.075
time_between_counts = 1  # (in seconds)  Default: 1

Count_Down_font = pygame.font.SysFont('Arial', 100)
Count_Down_fontS = pygame.font.SysFont('Arial', 60)
t_num = '---'
count_down_height_offset = -250

ACCENT_COL =  (102, 106, 111)
HIGHLIGHT_COL = 252, 192, 61
# Tweets
tweet_edge_thickness = 1
tweet_roundedcorner_radius = 10
tweet_bg_col = (8, 8, 8)

tweetfont = pygame.font.Font('fonts\\chirp-regular-web.woff', 20)
tweet_text_col = (231, 233, 234)
# tweet_text_pos = (300, 20)
tweet_linespace = 4

handlefont = pygame.font.Font('fonts\\chirp-regular-web.woff', 20)
handle_text_col = (102, 106, 111)
# handle_pos = (50, 100)

username_font = pygame.font.Font('fonts\\chirp-heavy-web.woff', 20)
username_text_col = (255, 255, 255)
username_pos = (90, 20)

pfp_s = 50
pfp_pos = (20, 20)


# Message Settings
message_font = pygame.font.SysFont('Calibri', 20)
time_font = pygame.font.SysFont('Calibri', 14)

