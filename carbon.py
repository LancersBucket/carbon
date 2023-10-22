import dearpygui.dearpygui as dpg
from pygame import mixer
import json

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

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=700, height=600)
dpg.setup_dearpygui()

# Soundboard Window
with dpg.window(label="Soundboard"):
    with dpg.group(horizontal=True):
        # Generate soundboard buttons
        for button in sbData["buttons"]:
            dpg.add_button(label=button["label"], callback=soundboard, height=75, width=75, tag="button"+str(button["id"]))
    
    # Stop and volume slider
    dpg.add_button(label="Stop", callback=stopSoundboard)
    volumeSlider = dpg.add_slider_int(label="Volume",callback=volumeSoundboard,min_value=0,max_value=100,default_value=50,clamped=True)

#demo.show_demo()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()