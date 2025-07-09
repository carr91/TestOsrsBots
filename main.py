from tinderBurn import *
from utils import *
import time

def chop_and_burn(n):
    """
    Runs the chop and burn routine:
    - click_yellow() + wait_for_xp_drop() 3 times
    - click_blue() once
    - wait 2 seconds
    - find_colors_and_click() + wait_for_xp_drop() 3 times
    """

    #for _ in range(n):
    #    click_yellow()
    #    wait_for_xp_drop()

    click_blue()
    time.sleep(5)

    for _ in range(n):
        find_colors_and_click()
        wait_for_xp_drop()

while(True):

    #chop_and_burn(10)

    while not is_inventory_full(threshold=.4):
        click_yellow()
        wait_for_xp_drop()
        time.sleep(1)
    click_blue()
    time.sleep(5)
    if is_inventory_full():
        while find_colors_and_click():
            wait_for_xp_drop()
