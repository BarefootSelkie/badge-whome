import badger2040
import jpegdec
import json
import os
import badger_os

# Global Constants
gScreenWidth = badger2040.WIDTH
gScreenHeight = badger2040.HEIGHT

# Where to find the json file with the parts in
gPartsPath = "/alt-parts/parts.json"

#This will only be displayed if something goes wrong, like no json file
gDefaultText = { "error":{ "name": "Error", "pronouns": "Err/or", "pips": "0", "tag":"Json file not found" } }

# This is the default state if nothing can be loaded from the state file
state = {
    "currentPart": 0
}

# Check to see if an image file exists for person, and if so return the path to it, if not return the path of the default image

def checkimage(name):
    path = "/alt-parts/" + name + ".jpg"
    try:
        os.stat(path)
        return path
    except OSError:
        path = "/alt-parts/default.jpg"
        return path
    
# --- Utility functions ---

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# --- Drawing ---

# Draw the screen, this uses pico graphics
def draw_screen(key):

    # Set font sizes
    nameSize = 2
    pronounSize = 1
    pipsSize = 0.5
    tagSize = 2

    # Set centre line of each line of text, from top of screen
    nameRow = 32
    pronounRow = 80
    tagRow = 100

    # Set the width of each area of text
    nameSpace = 296
    pronounSpace = 216
    tagSpace = 216

    # Blank the screen
    display.set_pen(15)
    display.clear()

    # Draw image
    jpeg.open_file(checkimage(key))
    # Place top right corner of the image in the bottom right 64 px of screen
    jpeg.decode(232, 64)

    # Draw the text
    display.set_pen(0)  # 0 is black, 15 is white
    display.set_font("sans")

    # Write the name on the screen
    display.set_thickness(4)
    nameWidth = display.measure_text(gParts[key]["name"], nameSize)
    nameIndent = (nameSpace - nameWidth) // 2
    display.text(gParts[key]["name"], nameIndent, nameRow, nameSpace, nameSize)

    # Write pronouns to screen
    display.set_thickness(2)
    pronounWidth = display.measure_text(gParts[key]["pronouns"], pronounSize)
    pronounIndent = ((pronounSpace - pronounWidth) // 2) + 16   
    display.text(gParts[key]["pronouns"], pronounIndent, pronounRow, pronounSpace, pronounSize)

    # Write tagline to screen, can use up to two lines
    display.set_font("bitmap6")
    display.text(gParts[key]["tag"], 18, tagRow, tagSpace, tagSize)

    # Display the correct number of pips in the bottom left corner
    # display.text(gParts[key]["pips"], 0, 120, 64, pipsSize)

    displayPips = 0
    
    # Check if pips are a number if so convert string to int, if not do nothing
    if gParts[key]["pips"].isdigit():
        displayPips = int(gParts[key]["pips"])

    for x in range(displayPips // 2):
        jpeg.open_file("/alt-parts/pip-full.jpg")
        jpeg.decode(0, 112 - (x * 16))
    if (displayPips % 2) is not 0: # if displayPips is odd
        jpeg.open_file("/alt-parts/pip-half.jpg")
        jpeg.decode(0, 112 - ((displayPips // 2) * 16))

    # Update the display
    display.update()

# --- Program setup ---

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

jpeg = jpegdec.JPEG(display.display)

badger_os.state_load("alt-parts", state)

changed = True

# ===  Main code ===

# Try to open the parts.json file
try:
    gParts = json.load(open(gPartsPath, "r"))
except OSError:
    gParts = gDefaultText
    pass

partCount = len(gParts)

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    if display.pressed(badger2040.BUTTON_UP):
        if state["currentPart"] > 0:
            state["currentPart"] -= 1
        else:
            state["currentPart"] = partCount - 1
        changed = True

    if display.pressed(badger2040.BUTTON_DOWN):
        if state["currentPart"] < partCount - 1:
            state["currentPart"] += 1
        else:
            state["currentPart"] = 0
        changed = True

    if display.pressed(badger2040.BUTTON_A):
        state["currentPart"] = 0
        changed = True

    if display.pressed(badger2040.BUTTON_B):
        state["currentPart"] = 1
        changed = True

    if display.pressed(badger2040.BUTTON_C):
        state["currentPart"] = 2
        changed = True

    if changed:
        draw_screen(list(gParts.keys())[state["currentPart"]])
        badger_os.state_save("alt-parts", state)
        changed = False

    # Halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
