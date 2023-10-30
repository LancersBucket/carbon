import os, sys, importlib
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import carbonmodulehelper as cmh
from pygame import mixer

depMode = False
depMod = None

config = cmh.readConfig("global")
sys.path.append(os.getcwd() + "\\"+config["carbon"]["moduleFolder"])
if (config["carbon"]["depMode"] is not False or None):
   depMode = True
   depMod = config["carbon"]["depMode"]

dpg.create_context()
dpg.create_viewport(title='Carbon', width=700, height=600)
dpg.setup_dearpygui()

# Module Loader
def dynamicModuleImport(module_name):
   try:
      load_module = importlib.import_module(module_name,os.getcwd()+"\\"+config["carbon"]["moduleFolder"]+"\\")
   except Exception as e:
      print("[CL] Error: "+str(e))
      return (False, None)
   try:
      load_module.init()
   except Exception as e:
      print("[CL] Error from module \'" +module_name+ "\': " + str(e))
   return (True, load_module)

# Generates an array of module data and human names
loaded_modules = []
module_names = []
for module in config["modules"]:
   try:
      if (config["modules"][module]["enable"] == False):
         continue
   except:
      pass
   out = dynamicModuleImport(module)
   if (config["modules"][module]["show"]):
      out[1].showWindow(True)
   if (out[0]):
      loaded_modules.append(out[1])
      module_names.append(module)

# Handles the regeneration of windows
def window_handler():
   if (not dpg.does_item_exist(dpg.get_value("Modules"))):
      loaded_modules[module_names.index(dpg.get_value("Modules"))].showWindow(show=True)
   else:
      loaded_modules[module_names.index(dpg.get_value("Modules"))].focusWindow()

# Load config file
#dpg.configure_app(init_file="dpg.ini")

# Supposed to lock window within viewport, will need to integrate and iterate
#def onMove():
#   dpg.set_item_pos("CL", [max(0,dpg.get_item_pos("CL")[0]),max(0,dpg.get_item_pos("CL")[1])])

# Main Carbon Loader Window. Helps open apps.
# Eventually I want to move CL to a seperate module but here it will stay
showCL = config["carbon"]["devMode"]
showCL = (showCL or depMode)
print(showCL)
with dpg.window(label="Carbon Loader",tag="CL",collapsed=showCL,show=(not showCL),no_open_over_existing_popup=False,width=200,height=200,on_close=dpg.delete_item("CL"),no_close=True):
   dpg.add_listbox(module_names,tag="Modules",callback=window_handler,width=dpg.get_item_width("CL")-15)
   dpg.add_text("Modules Loaded: " + str(len(loaded_modules)))
   dpg.add_text("DearPyGui: v" + str(dpg.get_dearpygui_version()))
   dpg.add_text("Carbon Loader: v1.5.1")

def showCarbonLoader(sender):
   dpg.focus_item("CL")
   # Why is the menu bar only 18 px tall?
   dpg.set_item_pos("CL",[0,19])

def showDemo():
   demo.show_demo()

if (not depMode):
   with dpg.viewport_menu_bar():
      dpg.add_menu_item(label=config["carbon"]["moduleLoader"], tag="Loader", callback=showCarbonLoader)
      dpg.add_menu_item(label="Demo Menu", tag="Demo Menu", callback=showDemo)

dpg.show_viewport()
if (depMode):
   loaded_modules[module_names.index(depMod)].showWindow(show=True)
   dpg.set_primary_window(config["carbon"]["depMode"],True)
dpg.start_dearpygui()
dpg.destroy_context()
try:
   mixer.stop()
   mixer.quit()
except:
   pass
finally:
   sys.exit()