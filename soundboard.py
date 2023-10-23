from pygame import mixer
import math, json
import dearpygui.dearpygui as dpg

mixer.init()

# Soundboard song player (uses soundboard.json to locate files)
def soundboard(sender):
    # Super brutal way to rip the numbers out of the id but it works
    soundid = int("".join(filter(str.isnumeric,sender)))
    mixer.music.load('files/'+sbData["buttons"][soundid]["file"])
    mixer.music.play()

# Stops the soundboard
def stopSoundboard():
    mixer.music.stop()

# Volume of soundboard
def volumeSoundboard():
    vol = dpg.get_value(volumeSlider)
    vol /= 100
    mixer.music.set_volume(vol)

# Get soundboard config
sbConf = open("soundboard.json")
sbData = json.load(sbConf)

def init(show=True):
    # Soundboard Window
    with dpg.window(label="Soundboard",show=show):
        width = 6
        total_length = len(sbData["buttons"])
        # Calculaltes how many rows are needed with given length
        rows = math.ceil(total_length / width)
        
        # Creates groups to put buttons
        groups = []
        for i in range(rows):
            groups.append(dpg.add_group(horizontal=True))

        # Adds buttons to each row, overflows to next row if space is needed
        for i in range(total_length):
            button = sbData["buttons"][i]
            currentRow = math.floor(i/(width))
            dpg.add_button(label=button["label"], callback=soundboard, height=75, width=75, tag="button"+str(button["id"]),parent=groups[currentRow])
        
        # Stop and volume slider
        dpg.add_button(label="Stop", callback=stopSoundboard)
        global volumeSlider
        volumeSlider = dpg.add_slider_int(label="Volume",callback=volumeSoundboard,min_value=0,max_value=100,default_value=50,clamped=True)
