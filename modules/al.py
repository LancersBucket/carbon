import dearpygui.dearpygui as dpg
import carbonmodulehelper as cmh
import json
import speech_recognition as sr

def destroy():
    dpg.delete_item("al")

def init():
    global r
    r = sr.Recognizer()
    global mic
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("ready")

    showWindow(True)
    dpg.focus_item("al")

def speak():
    with mic as source:
        audio = r.listen(source)
        print(r.recognize_google(audio,show_all=True))

def showWindow(show=False):
    with dpg.window(label="ALOS",tag="al",show=show,width=100,autosize=True,on_close=destroy):
        dpg.add_button(label="Speak",callback=speak)