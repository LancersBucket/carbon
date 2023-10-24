from pygame import mixer
import sys, os, random, configparser, yt_dlp
sys.path.append('../Carbon')
import carbonmodulehelper as cmh
import dearpygui.dearpygui as dpg

config = cmh.readConfig("shuffle")

def showMessage(msg):
    dpg.set_value("status",msg)

def shuffle(array):
    array = random.shuffle(array)

def playsong(self):
    try:
        # Gets the name of the file in the queue displays what is currently playing
        name = queue[currentPos]
        showMessage("[" + str(currentPos+1)+"/"+str(len(queue))+"] " + name[0:-4])

        # Loads the music and plays it
        mixer.music.load('music/'+name)
        mixer.music.set_volume(dpg.get_value("vol")/100)
        mixer.music.play()
    except:
        showMessage("Error: No songs are loaded.")

# Handles pausing and playing. Don't question it. I had to do it this way. I hope.
def playPauseButton(self):
    try:
        if not playing:
            playing = True
            if (paused):
                mixer.music.unpause()
                name = queue[currentPos]
                showMessage("[" + str(currentPos+1)+"/"+str(len(queue))+"] " + name[0:-4])
                paused = False
            else:
                playsong()
            dpg.set_value("Play","Pause")
        else:
            playing = False
            paused = True
            mixer.music.pause()
            dpg.set_value("Play","Play")
            showMessage("Paused")
    except:
        showMessage("Cannotp play, no songs are loaded.")


# Decrements the queue position
def backButton():
    mixer.music.stop()
    if (currentPos < 0):
        currentPos = len(queue)
    else:
        currentPos -= 1
    playsong()

# Increments the queue position
def forwardButton():
    if (currentPos >= len(queue)-1):
        mixer.music.stop()
        shuffle(queue)
        currentPos = 0
    else:
        currentPos += 1
    playsong()

# Monitors volume change
def volChange():
    mixer.music.set_volume(dpg.get_value("vol")/100)

# Reloads the queue and shuffles it
def shuffleButton():
    mixer.music.stop()

    queue = []
    songs = os.listdir('music')
    for song in songs:
        if (song.endswith(".mp3")):
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
    showWindow(True)
    dpg.focus_item("shuffle")

def showWindow(show=False):
    global queue
    queue = []
    global currentPos
    currentPos = 0
    global playing
    playing = False
    global paused
    paused = False
    with dpg.window(label="Shuffle",tag="shuffle",show=show,autosize=True,on_close=destroy):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Back",callback=backButton)
            dpg.add_button(label="Play",callback=playPauseButton)
            dpg.add_button(label="Forward",callback=forwardButton)
            dpg.add_button(label="Shuffle",callback=shuffleButton)
        dpg.add_slider_int(tag="vol",clamped=True,default_value=50,callback=volChange)
        dpg.add_text("HELP",tag="status")

    mixer.init()
    # Loads files into the queue
    if (not os.path.isdir('music')):
        os.mkdir('music')
    songs = os.listdir('music')
    for song in songs:
        if (song.endswith(".mp3")):
            queue.append(song)

    shuffle(queue)
    dpg.set_value("status","Ready. Queued " + str(len(queue)) + " songs.")
    if (queue == []):
        dpg.set_value("status","Error: No files found")
