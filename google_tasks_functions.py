import time

import pyautogui

from ui_lib import show_confirmation_dialog

def archive_task():
    """Archive a task in Google Tasks. Automate the process of right-clicking on a task and selecting "Archive"."""

    curr_pos = pyautogui.position()
    pyautogui.rightClick(*curr_pos)

    # TODO: this hardcoded position doesn't generally work. Need to find a better way to do this.
    archive_button_pos = curr_pos[0] + 20, curr_pos[1] - 120
    pyautogui.moveTo(*archive_button_pos)

    print('Asking for confirmation to archive the task')
    proceed = show_confirmation_dialog('Is the mouse in the correct position?\nand...\nAre you sure you want to archive this task?')

    if proceed:
        print('Clicking to give focus back to the web page')
        pyautogui.click(*archive_button_pos)
        print('Clicking on the "archive" button')
        pyautogui.click(*archive_button_pos)
    else:
        print('Clicking to give focus back to the web page')
        pyautogui.click(*archive_button_pos)
        print('Canceling the archive operation')


    time.sleep(0.1)
    pyautogui.moveTo(*curr_pos)

    return None