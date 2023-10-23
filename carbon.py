import math, json
import sys
import dearpygui.dearpygui as dpg
from pygame import mixer
import soundboard

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=700, height=600)
dpg.setup_dearpygui()

soundboard.initSoundboard()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()