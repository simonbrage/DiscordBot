# Miscellaneous commands

import random

def backflip_gif():
    gifs = ['https://giphy.com/gifs/justin-flipping-back-flip-jgflips-gczbF6nbRPVZ1YigE3',
            'https://giphy.com/gifs/officialfiym-forever-in-your-mind-fiym-xT0xetpPHT8UryiiqY',
            'https://giphy.com/gifs/fail-backflip-faceplant-sLFxTuBNHQfPW',
            'https://giphy.com/gifs/perfect-loops-3Wv7L5PaTBtAfrLSul',
            'https://giphy.com/gifs/espncfb-3oz8xUGwps7hlUMhaM']

    return random.choice(gifs)

def dice_roll():
    return random.randint(1, 6)

def custom_dice_roll(num):
    num = int(num)
    return random.randint(1, num)