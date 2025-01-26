import time
import threading
import subprocess

# for macOS ui elements
from Cocoa import NSAlert, NSApplication
from AppKit import NSRunningApplication, NSApplicationActivateIgnoringOtherApps

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
    

def show_confirmation_dialog(message: str = "Do you want to proceed?") -> bool:
    """Show a confirmation dialog with the given message.

    Args:
        message: The message to display in the dialog.

    Returns:
        True if the user clicks "Confirm", False if the user clicks "Cancel".
    """

    script = (f'tell application "System Events" to return button returned of '
              f'(display dialog "{message}" buttons {{"Cancel", "Continue"}} default button "Cancel")')
    try:
        # Redirect stderr to suppress error output
        result = subprocess.check_output(
            ['osascript', '-e', script],
            text=True,
            stderr=subprocess.DEVNULL  # Suppress stderr output
        ).strip()
    except subprocess.CalledProcessError:
        result = 'Cancel'

    if result == 'Continue':
        return True
    elif result == 'Cancel':
        return False
    
    # This approach is not working....

    # # Get the shared application instance
    # app = NSApplication.sharedApplication()

    # # Bring the application to the foreground
    # current_app = NSRunningApplication.currentApplication()
    # current_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # # Create an NSAlert instance
    # alert = NSAlert.alloc().init()
    # alert.setMessageText_(message)
    # alert.addButtonWithTitle_("Confirm")  # Add "Confirm" button
    # alert.addButtonWithTitle_("Cancel")  # Add "Cancel" button
    # alert.setAlertStyle_(0)  # 0 for informational style

    # # Start a background thread to set focus
    # # focus_thread = threading.Thread(target=set_focus_to_recent_python)
    # # focus_thread.start()

    # # Show the alert (this blocks the main thread)
    # response = alert.runModal()

    # app.stopModal()

    # # focus_thread.join()

    # # Handle the return value
    # if response == 1000:
    #     return True
    # elif response == 1001:
    #     return False

def set_focus_to_recent_python():
    """Set focus to the most recent Python process."""

    # Wait briefly to ensure the dialog has appeared
    time.sleep(0.1)

    # Use AppleScript to find and focus the most recent Python process
    script = '''
    tell application "System Events" to set frontmost of the last process whose name is "Python" to true
    '''
    subprocess.run(["osascript", "-e", script])

if __name__ == '__main__':
    print(show_confirmation_dialog())
