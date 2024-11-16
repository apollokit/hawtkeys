# hotkey_click

A tool for adding hot keys to a UI that doesn't have them. Just clicks in specific 
coordinates on the screen, so it's pretty bespoke.

hotkey_click.py works under MacOS. You can use it to enable a keyboard event to click somewhere on the screen

use "cmd+shift+4" to get the mouse position in MacOS. It shows the x,y coordinates, 

# Future work
1. add an app indicator icon that changes state based on the last hotkey acted upon (or create some other ui feedback that hotkey was acted upon)
1. use a yaml to specify the hotkeys and the x,y coordinates to click
1. allow hotkeys to use arbitrary modifiers
1. switch hotkey set based on the program that is focused in the ui
1. think about a more robust way to sense the location of buttons on the ui (use a screenshot and match pixels with a png?)

url: https://github.com/apollokit/hawtkeys