#!/bin/bash

# returns a string indicating the visibility status of an application window
# Usage: ./get_application_window_location.sh "Google Chat"
# -> 0: Window does not exist
# -> 1: Window is minimized
# -> 2: Window is visible and active
# -> 3: Window is (likely) obscured by other windows

app_name=$1

echo $(osascript -e "
tell application \"System Events\"
    tell application process \"$app_name\"
        if not (exists window 1) then
            return 0
        else if (value of attribute \"AXMinimized\" of window 1) then
            return 1
        else if frontmost then
            return 2
        else
            return 3
        end if
    end tell
end tell
")