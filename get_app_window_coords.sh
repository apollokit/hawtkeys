#!/bin/bash

# returns the position and size of an application window
# Usage: ./get_application_window_location.sh "Google Chat"
# -> 1920, 32, 1728, 1085  (x,y,width,height)

app_name=$1

echo $(osascript -e "
tell application \"System Events\"
    tell application process \"$app_name\"
        tell (first window)
            set winBounds to position & size
        end tell
    end tell
end tell
return winBounds
")