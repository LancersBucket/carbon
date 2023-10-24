from pygame import mixer
import math, json, os
import dearpygui.dearpygui as dpg
import carbonmodulehelper as cmh

# Soundboard song player (uses soundboard.json to locate files)
def soundboard(sender):
    # Super brutal way to rip the numbers out of the id but it works
    soundid = int("".join(filter(str.isnumeric,sender)))
    mixer.music.load(sbData["soundFolder"]+'/'+sbData["buttons"][soundid]["file"])
    mixer.music.play()

# Stops the soundboard
def stopSoundboard():
    mixer.music.stop()

# Volume of soundboard
def volumeSoundboard():
    vol = dpg.get_value(volumeSlider)
    vol /= 100
    mixer.music.set_volume(vol)

# Destroy function of window
def destroy():
    mixer.quit()
    dpg.delete_item("window")

# Get soundboard config
sbData = cmh.readConfig("soundboard")
Data = cmh.readConfig("global")

if (sbData["regenConfig"] == True):
    Data["modules"]["soundboard"]["regenConfig"] = False
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
    pass

def init(show=False):
    mixer.init()
    # Soundboard Window
    with dpg.window(label="Soundboard",tag="window",show=show,width=100,autosize=True,on_close=destroy):
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
            dpg.add_button(label=button["label"], callback=soundboard, height=75, width=150, tag="button"+str(button["id"]),parent=groups[currentRow])
        
        # Stop and volume slider
        dpg.add_button(label="Stop", callback=stopSoundboard)
        global volumeSlider
        volumeSlider = dpg.add_slider_int(label="Volume",callback=volumeSoundboard,min_value=0,max_value=100,default_value=50,clamped=True)
