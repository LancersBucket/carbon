# TODO: Update shuffle to use mixer functions instead of custom functions
# https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music
# TODO: Add D&D Sound Module (Mythril)
from pygame import mixer
import sys, os, random
sys.path.append('../Carbon')
import carbonmodulehelper as cmh
import dearpygui.dearpygui as dpg

def showMessage(msg):
    dpg.set_value("shuffleStatus",msg)

def shuffle(array):
    array = random.shuffle(array)

def playsong():
    global queue
    global currentPos
    global playing
    global config
    try:
        # Gets the name of the file in the queue displays what is currently playing
        name = queue[currentPos]
        showMessage("[" + str(currentPos+1)+"/"+str(len(queue))+"] " + name.split(" [")[0])
        # Loads the music and plays it
        mixer.music.load(config["musicFolder"]+ '/'+name)
        mixer.music.set_volume(dpg.get_value("shuffleVol")/100)
        mixer.music.play()
    except:
        showMessage("Error: No songs are loaded.")

# Handles pausing and playing. Don't question it. I had to do it this way. I hope.
def playPauseButton():
    try:
        global playing
        global paused
        global currentPos
        if not playing:
            playing = True
            if (paused):
                mixer.music.unpause()
                name = queue[currentPos]
                showMessage("[" + str(currentPos+1)+"/"+str(len(queue))+"] " + name.split(" [")[0])
                paused = False
            else:
                playsong()
            dpg.set_item_label("shufflePlay","Pause")
        else:
            playing = False
            paused = True
            mixer.music.pause()
            dpg.set_item_label("shufflePlay","Play")
            showMessage("Paused")
    except:
        showMessage("Cannot play, no songs are loaded.")


# Decrements the queue position
def backButton():
    global currentPos
    global queue
    mixer.music.stop()
    if (currentPos < 0):
        currentPos = len(queue)
    else:
        currentPos -= 1
    playsong()

# Increments the queue position
def forwardButton():
    global currentPos
    global queue
    if (currentPos >= len(queue)-1):
        mixer.music.stop()
        shuffle(queue)
        currentPos = 0
    else:
        currentPos += 1
    playsong()

# Monitors volume change
def volChange():
    mixer.music.set_volume(dpg.get_value("shuffleVol")/100)

# Reloads the queue and shuffles it
def shuffleButton():
    global queue
    global currentPos
    mixer.music.stop()

    queue = []
    songs = os.listdir(config["musicFolder"])
    for song in songs:
        if (song.endswith((".mp3",".mid",".wav"))):
            queue.append(song)

    shuffle(queue)
    currentPos = 0
    playsong()

def destroy():
    mixer.quit()
    dpg.delete_item("shuffle")

def focusWindow():
    dpg.focus_item("shuffle")

def init():
    global config
    config = cmh.getConfig("shuffle")
    global currentPos
    currentPos = 0
    global queue
    queue = []
    global playing
    playing = False
    global paused
    paused = False

def showWindow(show=False):
    with dpg.window(label="Shuffle",tag="shuffle",show=show,autosize=True,on_close=destroy):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Back",callback=backButton)
            dpg.add_button(label="Play",tag="shufflePlay",callback=playPauseButton)
            dpg.add_button(label="Forward",callback=forwardButton)
            dpg.add_button(label="Shuffle",callback=shuffleButton)
        dpg.add_slider_int(tag="shuffleVol",clamped=True,default_value=50,callback=volChange)
        dpg.add_text("HELP",tag="shuffleStatus")

    mixer.init()
    # Loads files into the queue
    songs = cmh.checkFolder(config["musicFolder"],True,True)
    for song in songs:
        if (song.endswith((".mp3",".mid",".wav"))):
            queue.append(song)

    shuffle(queue)
    dpg.set_value("shuffleStatus","Ready. Queued " + str(len(queue)) + " songs.")
    if (queue == []):
        dpg.set_value("shuffleStatus","Error: No files found")
    dpg.set_item_pos("shuffle",[0,19])