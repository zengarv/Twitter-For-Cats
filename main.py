# This is for the things the thingy needs to thing properly
import pygame
from Settings import *
screen = pygame.display.set_mode((WIDTH, HEIGHT))
from ManagersAndMenus import TweetManager, load_screen, BurgerMenu

# Wow so cool initializing and stuff
pygame.init()
pygame.display.set_caption('TwitterForCats')
pygame.display.set_icon(GRUMPS)
load_screen(screen, pygame.font.Font('fonts\\chirp-regular-web.woff', 40))
clock = pygame.time.Clock()

from ManagersAndMenus2 import Piano, CountCats
from ManagersAndMenus3 import Catroom
from Miscellaneous import Rat, SelfDestruct, Paw
from fireworks import *


SD = SelfDestruct(screen)
BM = BurgerMenu(screen, [[TweetManager(screen, (0, 80)), "Tweets", r'cats\grumps.png'], [Piano(screen, (0, 95)), "Piano", r'images\icons\piano.png'], [CountCats(screen, (0, 95)), "SleepyTime", r'images\icons\sleepycat.png'], [Catroom(screen, (0, 95)), "CatChat", r'images\icons\Catchat.png']])
grumps_icon = pygame.transform.smoothscale(pygame.transform.flip(pygame.image.load(r'cats\grumps.png'), True, False), (55, 55))
grumps_icon_rect = grumps_icon.get_rect()
grumps_icon_rect.midright = WIDTH-10, 40
l = pygame.transform.smoothscale(logo, (1920//6, 194//6))
l_rect = l.get_rect()
l_rect.center = WIDTH//2, 40

rat = Rat(screen)   
BOMB.convert_alpha()

# This is the main thing
paw = Paw(paw_cursor, screen)

def shutdown():
    BM.menus[3].send_to_server(DISCONNECT_MESSAGE)

run = True
fireworks = []
dt = 1/FPS
while run:
    # Idk man this is pretty boring to document
    mouse_pos = pygame.mouse.get_pos() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SD.initiate_self_destruct_sequence()
        
        elif event.type == pygame.VIDEORESIZE: 
            WIDTH, HEIGHT = event.size
        
        elif event.type == pygame.MOUSEMOTION:
            BM.hover(event.pos)     
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If Clicky click
            if event.button == 1:
                # Do click stuff
                paw.click(event.pos)
                if rat.click(event.pos) and enable_fireworks:
                    f = Firework(event.pos[0], [0, -800], r_c(), y=event.pos[1], screen=screen)
                    f.explode()
                    fireworks.append(f)
                if grumps_icon_rect.collidepoint(event.pos): g_meow.play()
                else:
                    BM.click(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                BM.mouse_button_up(event.pos)
             
        elif event.type == pygame.MOUSEWHEEL:
            # If mouse goes weeeeeee, do more stuff
            BM.scroll((event.x, event.y), mouse_pos) 
             
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:      # Esc key
                run = False
                shutdown()
                
            elif event.key == 32 and BM.selected_menu_index != 3:    # Long Boi   # Disables missile systems in chat (the cats are friendly to each other)
                paw.keydown(mouse_pos)
            
            BM.keydown(event)
                
        elif event.type == pygame.KEYUP:
            if event.key == 32 and BM.selected_menu_index != 3:
                paw.keyup()   
            BM.keyup(event)
            
    screen.fill(tweet_bg_col)

    screen.blit(l, l_rect)
    
    BM.update(dt, mouse_pos)
    BM.draw()

    for m in paw.missiles:
        if rat.exist and not m.has_exploded and m.rot_surf_rect.colliderect(rat.rot_rect):
            rat.kill()
            m.explode()
            break
    
    if enable_fireworks:
        for f in fireworks:      
            f.update(dt)  
            f.draw()
            
            if len(f.particles) == 0 and f.exploded:
                fireworks.remove(f)
        
    fps = clock.get_fps()
    dt=1/fps if not fps == 0 else 1/FPS
    
    if SD.update(dt): run = False
    SD.draw()
    
    rat.update(dt)   
    if not SD.initiated: rat.draw()
    
    screen.blit(grumps_icon, grumps_icon_rect)
    
    if show_FPS: screen.blit(fps_font.render(f'{fps:0.2f}', True, (25, 190, 48)), (550, 20))
        
    paw.update(dt, mouse_pos)
    pygame.display.update()
    clock.tick(FPS)
        
    
pygame.quit()

# End of Sauce, Pass the Chips   