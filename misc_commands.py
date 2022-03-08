# Miscellaneous commands

import random

def backflip_gif():
    from resources.gifs import gifs

    return random.choice(gifs)

def dice_roll():
    return random.randint(1, 6)

def custom_dice_roll(num):
    num = int(num)
    return random.randint(1, num)