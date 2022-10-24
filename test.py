# These are just tools used to create, edit or save assets so they can be used more efficiently in the main program
# These were required only at the time of development and can be safely ignored at runtime
# (These libraries need not be installed for the functioning of the main program)

from PIL import Image
from itertools import product
import os

def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)
    
# tile('explosion_spritesheet.png', 'images', 'images', 256)

def cat_rename():
    for f in range(1, 17):
        files = os.listdir(f'images\\cat\\{f}')
        for file in files:
            li = list(map(lambda x: x//48, list(map(int, file.strip('.png').split('_')[1:]))))
            os.rename(f'images\\cat\\{f}\\{file}', f'images\\cat\\{f}\\{li[0]} {li[1]}.png')


def extract_from_gif(path):
    with Image.open(path) as im:
        num_key_frames = im.n_frames
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            im.save('{}.png'.format(i))