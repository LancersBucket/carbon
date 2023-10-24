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
      return (False, None)
   return (True, load_module)

loaded_modules = []
module_names = []
for module in config["modules"]:
   out = dynamic_module_import(module)
   if (out[0]):
      loaded_modules.append(out[1])
      module_names.append(module)

def window_handler(windowName):
   loaded_modules[module_names.index(dpg.get_value("Modules"))].init()


with dpg.window(label="Carbon Loader",show=True,no_open_over_existing_popup=False,width=200,height=300):
   dpg.add_text("Carbon")
   dpg.add_listbox(module_names,id="Modules",callback=window_handler)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()