import math, json
import sys
import dearpygui.dearpygui as dpg
from pygame import mixer
#import soundboard
import importlib

file = open("carbonConfig.json")
config = json.load(file)

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=700, height=600)
dpg.setup_dearpygui()

import imp
import sys

# function to dynamically load module
def dynamic_module_import(module_name):
   # find_module() is used to find the module in current directory
   # it gets the pointer, path and description of the module
   try:
      file_pointer, file_path, description = imp.find_module(module_name)
   except ImportError:
      print("Imported module {} not found".format(module_name))
   try:
      # load_module dynamically loads the module
      # the parameters are pointer, path and description of the module 
      load_module = imp.load_module(module_name, file_pointer, file_path, description)
      load_module.init()
   except Exception as e:
      print(e)
   #return load_module

for module in config["modules"]:
   dynamic_module_import(module)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()