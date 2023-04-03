""" Move the cursor around the screen on a loop to keep the computer awake.

Note: use "cmd+shift+4" to get the mouse position. It shows the x,y coordinates, 
 the bookwhich can be used with pyautogui.click(x,y)
"""

import time

import pyautogui

poss = [
    (500,350),
    (500,750),
    (1400,750),
    (1400,350),
]

indx = 0
curr_pos = poss[indx]

while True:
    print(f'Move to {curr_pos}')
    pyautogui.moveTo(*curr_pos)

    indx += 1
    indx %= len(poss)
    curr_pos = poss[indx]

    time.sleep(10)