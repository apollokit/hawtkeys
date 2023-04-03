""" Use a hot key to click on the screen on MacOS

Note: use "cmd+shift+4" to get the mouse position. It shows the x,y coordinates, 
 the bookwhich can be used with pyautogui.click(x,y)

A lot of this code came from keyboard.py in better_dictate, 
"""
from typing import Union
import time

import pyautogui
from pynput import keyboard

class KeyboardManager():

    def on_press(self, key: keyboard.KeyCode):
        # if str(key) in keys_for_parser:
        #     # print("setting key_pressed_parser_event")
        #     key_pressed_parser_event.set()
        pass


    def on_release(self,
        key: Union[keyboard.KeyCode, keyboard.Key]):
        """ Takes action upon key release.

        Args:
            key: the key that was released
        """
        keystring = str(key).strip('\'')

        # for restoring current position after clicking
        curr_pos = pyautogui.position()
        
        ## for kicad UI buttons

        ## pcbnew
        # these work on my hp monitor at home, with the pcbnew window maximized
        # alt+b -> button for "show filled areas in zones"
        if keystring == 'Ω':
            print(f'Saw {keystring} hotkey, show filled areas in zones')
            pyautogui.click(16,400)
            pyautogui.moveTo(*curr_pos)
        # alt+n -> button for "do not show filled areas in zones"
        elif keystring == '≈':
            print(f'Saw {keystring} hotkey, do not show filled areas in zones')
            pyautogui.click(16,435)
            pyautogui.moveTo(*curr_pos)
        elif keystring == '∫':
            print(f'Saw {keystring} hotkey, click connection type')
            pyautogui.click(750,412)
            pyautogui.moveTo(*curr_pos)
        elif keystring == '˜':
            print(f'Saw {keystring} hotkey, click okay')
            pyautogui.click(1111,661)
            pyautogui.moveTo(*curr_pos)

if __name__ == '__main__':

    kb_mngr = KeyboardManager()

    keyb_listener = keyboard.Listener(
        on_press=kb_mngr.on_press,
        on_release=kb_mngr.on_release)

    keyb_listener.start()

    while True:
        time.sleep(1)