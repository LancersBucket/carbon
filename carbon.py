import math, json
import sys
import dearpygui.dearpygui as dpg
from pygame import mixer
import importlib

file = open("carbonConfig.json")
config = json.load(file)

dpg.create_context()
dpg.create_viewport(title='Carbon', width=700, height=600)
dpg.setup_dearpygui()

# function to dynamically load module
def dynamic_module_import(module_name):
   try:
      load_module = importlib.import_module(module_name)
      
      # Run module initilization
      load_module.init()
   except Exception as e:
      print(e)

for module in config["modules"]:
   dynamic_module_import(module)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()