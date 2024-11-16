""" Use a hot key to click on the screen on MacOS

Note: use "cmd+shift+4" to get the mouse position. It shows the x,y coordinates, 
 the bookwhich can be used with pyautogui.click(x,y)

A lot of this code came from keyboard.py in better_dictate, 
"""
import click
from typing import Union
import time
import subprocess

import pyautogui
from pynput import keyboard

WINDOW_IS_VISIBLE_AND_ACTIVE = 2

class KeyboardManager():

    def __init__(self, mode: str):
        self.mode = mode
        # current_keys is a set of keys that are currently being pressed -
        #  will be cleared on_release
        self.current_keys: set[keyboard.Key] = set()

    def on_press(self, key: keyboard.KeyCode):
        # if str(key) in keys_for_parser:
        #     # print("setting key_pressed_parser_event")
        #     key_pressed_parser_event.set()
        self.current_keys.add(key)

    def on_release(self,
        key: Union[keyboard.KeyCode, keyboard.Key]):
        """ Takes action upon key release.

        Args:
            key: the key that was released
        """
        keystring = str(key).strip('\'')
        current_keys = self.current_keys

        # for restoring current position after clicking
        curr_pos = pyautogui.position()

        if self.mode == 'standard':
            # alt+b -> move to center of screen
            if keystring == '∫':
                print(f'Saw {keystring} hotkey, move to center of screen')
                pyautogui.moveTo(950,500)
            # cmd+shift+k -> click at location (80,150)  (intended for "new chat" button in gchat)
            elif {    keyboard.Key.cmd, 
                    keyboard.Key.shift, 
                    keyboard.KeyCode(char='k')}.issubset(current_keys):

                print(f'Saw {keystring} hotkey, Google Chat new chat button hotkey')
                status = get_window_viz_status("Google Chat")

                if status == WINDOW_IS_VISIBLE_AND_ACTIVE:
                    posx, posy, width, height = get_window_position("Google Chat")
                    clickx = posx + 60
                    clicky = posy + 150
                    print(f'\tWindow is active, click at location ({clickx}, {clicky}) ("new chat" button in gchat)')
                    pyautogui.moveTo(clickx,clicky)
                    time.sleep(0.01)
                    pyautogui.click(clickx,clicky)
                    pyautogui.moveTo(*curr_pos)
                else:
                    print('\tWindow is not active, do nothing')

        ## for kicad UI buttons
        elif self.mode == 'pcbnew':
            ## pcbnew
            # these work on my hp monitor at home, with the pcbnew window maximized
            # alt+z -> button for "show filled areas in zones"
            if keystring == 'Ω':
                print(f'Saw {keystring} hotkey, show filled areas in zones')
                pyautogui.click(16,400)
                pyautogui.moveTo(*curr_pos)
            # alt+n -> button for "do not show filled areas in zones"
            elif keystring == '≈':
                print(f'Saw {keystring} hotkey, do not show filled areas in zones')
                pyautogui.click(16,435)
                pyautogui.moveTo(*curr_pos)
            # alt+b
            elif keystring == '∫':
                print(f'Saw {keystring} hotkey, click connection type')
                pyautogui.click(750,412)
                pyautogui.moveTo(*curr_pos)
            # alt+n 
            elif keystring == '˜':
                print(f'Saw {keystring} hotkey, click okay')
                pyautogui.click(1111,661)
                pyautogui.moveTo(*curr_pos)
        
        ## for gmail cleaning
        elif self.mode == 'gmail':
            # alt+z -> delete label
            if keystring == 'Ω':
                print(f'Saw {keystring} hotkey, delete label')
                pyautogui.click(1290,585)
                time.sleep(0.1)
                pyautogui.click(1050,650)

        else:
            raise ValueError(f'Unknown mode {self.mode}')
        
        self.current_keys.discard(key)

def get_window_viz_status(app_name) -> int | None:
    """Get the visibility status of the window of the given application.
    
    See the shell script get_app_window_viz_status.sh for more details.
    """

    # Call the shell script with the application name as an argument
    result = subprocess.run(
        ['./get_app_window_viz_status.sh', app_name],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True  # Decode output as text
    )

    # Check if the script executed successfully
    if result.returncode == 0:
        # Parse and return the output
        return int(result.stdout)
    else:
        # Handle errors (if any)
        print(f"Error: {result.stderr.strip()}")
        return None

def get_window_position(app_name) -> tuple[int,int,int,int] | None:
    """Get the position of the top-left corner of the window of the given application."""

    # Call the shell script with the application name as an argument
    result = subprocess.run(
        ['./get_app_window_coords.sh', app_name],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True  # Decode output as text
    )

    # Check if the script executed successfully
    if result.returncode == 0:
        # Parse and return the output
        return (int(res) for res in result.stdout.strip().split(','))
    else:
        # Handle errors (if any)
        print(f"Error: {result.stderr.strip()}")
        return None

@click.group() # type: ignore
def cli():
    pass

MODES = ['standard', 'pcbnew']

@cli.command()
@click.argument('mode', default='standard')
def go(mode: str):
    kb_mngr = KeyboardManager(mode)

    keyb_listener = keyboard.Listener(
        on_press=kb_mngr.on_press,
        on_release=kb_mngr.on_release)

    keyb_listener.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    cli()
    