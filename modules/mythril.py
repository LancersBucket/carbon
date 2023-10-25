import sys, random, os
from math import ceil, floor
from time import sleep
from pygame import mixer, USEREVENT
sys.path.append('../Carbon')
import carbonmodulehelper as cmh
import dearpygui.dearpygui as dpg
import threading
import pygame
from mutagen.mp3 import MP3

loop = False
fade = False
SONGEND = USEREVENT+1
currentSong = ""
alive = True
shuffle = False
songLength = -1

def showMessage(msg):
    dpg.set_value("status",msg)

def forwardButton():
    global currentBank
    global currentSong
    mixer.music.stop()
    currentBankItems = dpg.get_item_user_data(currentBank+"List")
    index = currentBankItems.index(currentSong)
    if (not shuffle):
        if ((index + 1) > len(currentBankItems)-1):
            index = 0
        else:
            index += 1
    else:
        index = random.randrange(0, len(currentBankItems)-1)
    newSong = currentBankItems[index]
    dpg.set_value(currentBank+"List",newSong)
    playPauseButton()

def backButton():
    global currentBank
    global currentSong
    mixer.music.stop()
    currentBankItems = dpg.get_item_user_data(currentBank+"List")
    index = currentBankItems.index(currentSong)

    if ((index - 1) < 0):
        index = len(currentBankItems)-1
    else:
        index -= 1
    newSong = currentBankItems[index]
    dpg.set_value(currentBank+"List",newSong)
    playPauseButton()

def playSong():
    global queue
    global currentPos
    global playing
    global config
    global currentBank
    global currentSong
    global songLength
    try:
        currentSong = dpg.get_value(currentBank+"List")
        mixer.music.unload()
        # Loads the music and plays it
        mixer.music.load(config["musicFolder"]+ '/'+currentBank+'/'+currentSong)
        mixer.music.set_endevent(SONGEND)
        volChange()
        song = MP3(config["musicFolder"]+ '/'+currentBank+'/'+currentSong)
        songLength = song.info.length*1000
        print(songLength)
        mixer.music.play(fade_ms=(int(fade)*config["fadeTimeMS"]))

    except Exception as e:
        showMessage("Error: No songs are loaded.")
        print(e)

def playPauseButton(swapState = False):
    try:
        global playing
        global paused
        global currentPos
        if not playing:
            playing = True
            if (paused):
                print("nowPlaying")
                mixer.music.unpause()
                paused = False
                showMessage("Now playing: " + currentSong)
            else:
                mixer.music.unload()
                playSong()
                showMessage("Now playing: " + currentSong)
            dpg.set_item_label("play","Pause")
        else:
            playing = False
            paused = True
            mixer.music.pause()
            dpg.set_item_label("play","Play")
            showMessage("Paused")
    except:
        showMessage("Cannot play, no songs are loaded.")

# Monitors volume change
def volChange():
    mixer.music.set_volume(dpg.get_value("vol")/100)

def selectBank(sender=""):
    global paused
    paused = True
    global playing
    playing = False
    global currentBank
    global currentSong
    if (fade):
        showMessage("Fading Song...")
        mixer.music.fadeout(config["fadeTimeMS"])
    else:
        mixer.music.stop()
    mixer.music.unload()
    dpg.set_item_label("play","Play")
    if (not currentBank == ""):
        dpg.configure_item(currentBank+"Text",color=(255,0,0,255))
    item = sender.split("Button")
    currentBank = item[0]
    currentBankItems = dpg.get_item_user_data(currentBank+"List")
    dpg.configure_item(item[0]+"Text",color=(0,255,0,255))
    showMessage("Selected bank: " + currentBank)
    currentSong = currentBankItems[0]
    paused = False

def checkStatus():
    global playing
    global paused
    global alive
    while alive:
        sleep(0.1)
        try:
            dpg.set_value("seek",pygame.mixer.music.get_pos())
            dpg.configure_item("seek",max_value=songLength)
        except:
            pass

        for event in pygame.event.get():
            if event.type == SONGEND:
                print("did somethin")
                playing = False
                paused = False
                try:
                    mixer.music.unload()
                except:
                    pass
                if (not loop):
                    forwardButton()
                else:
                    playPauseButton()
                

def destroy():
    global t1
    global alive
    mixer.quit()
    dpg.delete_item("mythril")
    alive = False
    t1.join()
    print(t1.is_alive())

def init():
    global config
    config = cmh.readConfig("mythril")
    global currentPos
    currentPos = 0
    global tags
    tags = []
    global queue
    queue = []
    global playing
    playing = False
    global paused
    paused = False
    global currentBank
    currentBank = ""
    pygame.init()
    showWindow(True)
    dpg.focus_item("mythril")
    global t1
    t1 = threading.Thread(target=checkStatus,args=(),daemon=True)
    t1.start()

def flipFade():
    global fade 
    fade = not fade

def flipLoop():
    global loop
    loop = not loop

def flipShuffle():
    global shuffle
    shuffle = not shuffle

def swapSong():
    pass

def showWindow(show=False):
    global tags
    global currentBank
    global fade

    mixer.init()
    # Loads files into the queue
    if (not os.path.isdir(config["musicFolder"])):
        os.mkdir(config["musicFolder"])
    folders = os.listdir(config["musicFolder"])
    for tag in folders:
        if (tag.find(".") == -1):
            tags.append(tag)

    with dpg.window(label="Mythril",tag="mythril",show=show,autosize=True,on_close=destroy):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Back",callback=backButton)
            dpg.add_button(label="Play",tag="play",callback=playPauseButton)
            dpg.add_button(label="Forward",callback=forwardButton)
        dpg.add_slider_int(tag="vol",clamped=True,default_value=50,callback=volChange)
        dpg.add_slider_float(tag="seek",clamped=True,no_input=True)
        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="Loop Current Song",callback=flipLoop)
            dpg.add_checkbox(label="Fade Between Songs",callback=flipFade)
            dpg.add_checkbox(label="Shuffle",callback=flipShuffle)

        width = 2
        total_length = len(tags)
        # Calculaltes how many rows are needed with given length
        rows = ceil(total_length / width)

        # Creates groups to put buttons
        groups = []
        for i in range(rows):
            groups.append(dpg.add_group(horizontal=True))

        # Adds buttons to each row, overflows to next row if space is needed
        for i in range(total_length):
            label = tags[i]
            currentRow = floor(i/(width))
            dpg.add_group(tag=label,parent=groups[currentRow],horizontal=False)
            dpg.add_text(label,parent=label,color=(255,0,0,255),tag=(label+"Text"))
            tagSongs = []
            for song in os.listdir(config["musicFolder"]+"/"+label):
                tagSongs.append(song)
            dpg.add_listbox(tagSongs,parent=label,tag=(label+"List"),user_data=tagSongs,callback=swapSong)
            dpg.add_button(label="Select",parent=label,tag=(label+"Button"),callback=selectBank)
        dpg.add_text("HELP",tag="status")
        selectBank(tags[0])