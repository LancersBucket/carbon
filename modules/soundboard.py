import json, os, sys
from pygame import mixer
from math import ceil, floor
import dearpygui.dearpygui as dpg
# Dirty fix to access carbonmodule
sys.path.append('../Carbon')
import carbonmodulehelper as cmh

playingSound = None

# Soundboard song player (uses soundboard.json to locate files)
def soundboard(sender):
    # Super brutal way to rip the numbers out of the id but it works
    soundid = int("".join(filter(str.isnumeric,sender)))
    global playingSound
    playingSound = mixer.Sound(sbData["soundFolder"]+'/'+sbData["buttons"][soundid]["file"])
    playingSound.set_volume(dpg.get_value(volumeSlider)/100)
    mixer.Channel(0).play(playingSound)

# Stops the soundboard
def stopSoundboard():
    mixer.stop()

# Volume of soundboard
def volumeSoundboard():
    vol = dpg.get_value(volumeSlider)
    vol /= 100
    try:
        playingSound.set_volume(vol)
    except:
        pass

# Destroy function of window
def destroy():
    mixer.quit()
    dpg.delete_item("soundboard")

def focusWindow():
    dpg.focus_item("soundboard")

def init():
    # Get soundboard config
    global sbData
    sbData = cmh.readConfig("soundboard")
    
    Data = cmh.readConfig("global")
    
    # This will need to be moved to cmh
    if (sbData["regenButtons"] == True):
        Data["modules"]["soundboard"]["regenButtons"] = False
        Data["modules"]["soundboard"].pop("buttons")
        Data["modules"]["soundboard"]["buttons"] = []
        
        counter = 0
        for f in os.listdir("files"):
            Data["modules"]["soundboard"]["buttons"].append({"id":counter,"label":f.split(" [")[0],"file":f})
            counter += 1

        newData = json.dumps(Data, indent=4)

        with open('carbonConfig.json', 'w') as file:
            # write
            file.write(newData)

def showWindow(show=False):
    mixer.init()
    # Soundboard Window
    with dpg.window(label="Soundboard",tag="soundboard",show=show,width=100,autosize=True,on_close=destroy):
        width = sbData["buttonsPerRow"]
        total_length = len(sbData["buttons"])
        # Calculaltes how many rows are needed with given length
        rows = ceil(total_length / width)
        
        # Creates groups to put buttons
        groups = []
        for i in range(rows):
            groups.append(dpg.add_group(horizontal=True))

        # Adds buttons to each row, overflows to next row if space is needed
        for i in range(total_length):
            button = sbData["buttons"][i]
            currentRow = floor(i/(width))
            dpg.add_button(label=button["label"], callback=soundboard, height=75, width=150, tag="button"+str(button["id"]),parent=groups[currentRow])
        
        # Stop and volume slider
        dpg.add_button(label="Stop", callback=stopSoundboard)
        global volumeSlider
        volumeSlider = dpg.add_slider_int(label="Volume",callback=volumeSoundboard,min_value=0,max_value=100,default_value=50,clamped=True)
