import os, sys, importlib
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import carbonmodulehelper as cmh

config = cmh.getConfig("global")

depMode = False
depModule = None
if (cmh.readValue(config["carbon"],"depMode",False) is not False or None):
   depMode = True
   depModule = config["carbon"]["depMode"]

showCL = cmh.readValue(config["carbon"],"devMode",False) or depMode

moduleFolder = cmh.readValue(config["carbon"],"moduleFolder","modules")

sys.path.append(os.getcwd() + "\\"+moduleFolder)

dpg.create_context()
dpg.create_viewport(title='Carbon', width=700, height=600)
dpg.setup_dearpygui()

# Module Loader
def dynamicModuleImport(module_name):
   try:
      load_module = importlib.import_module(module_name,os.getcwd()+"\\"+moduleFolder+"\\")
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
   if (depMode and not (module == depModule)):
      continue
   if (not cmh.readValue(config["modules"][module],"enable",failReturn=True)):
      continue
   loaded, loaded_module = dynamicModuleImport(module)
   
   if (cmh.readValue(config["modules"][module],"show")):
      try:
         loaded_module.showWindow(True)
      except Exception as e:
         print("[CL] Error from module \'" +str(module)+ "\': " + str(e))
   if (loaded):
      loaded_modules.append(loaded_module)
      module_names.append(module)

# Handles the regeneration of windows
def window_handler():
   try:
      module_name = dpg.get_value("Modules")
      if (not dpg.does_item_exist(module_name)):
         loaded_modules[module_names.index(module_name)].showWindow(show=True)
      else:
         loaded_modules[module_names.index(module_name)].focusWindow()
   except Exception as e:
      print("[CL] Error from module \'" +str(module_name)+ "\': " + str(e))

# Load config file
#dpg.configure_app(init_file="dpg.ini")

# Supposed to lock window within viewport, will need to integrate and iterate
#def onMove():
#   dpg.set_item_pos("CL", [max(0,dpg.get_item_pos("CL")[0]),max(0,dpg.get_item_pos("CL")[1])])

# Main Carbon Loader Window. Helps open apps.
# Eventually I want to move CL to a seperate module but here it will stay
with dpg.window(label="Carbon Loader",tag="CL",collapsed=showCL,show=(not showCL),no_open_over_existing_popup=False,width=200,height=200,on_close=dpg.delete_item("CL"),no_close=True):
   dpg.add_listbox(module_names,tag="Modules",callback=window_handler,width=dpg.get_item_width("CL")-15,num_items=len(loaded_modules))
   dpg.add_text("Modules Loaded: " + str(len(loaded_modules)))
   dpg.add_text("DearPyGui: v" + str(dpg.get_dearpygui_version()))
   dpg.add_text("Carbon Loader: v1.6.0")

def showCarbonLoader():
   dpg.focus_item("CL")
   # Why is the menu bar only 18 px tall? Beats me.
   dpg.set_item_pos("CL",[0,19])

if (not depMode):
   cmh.addMenuBarItem(cmh.readValue(config["carbon"],"moduleLoader","Carbon Loader"), tag="Loader", callback=showCarbonLoader)
   cmh.addMenuBarItem("Demo Menu", tag="Demo Menu", callback=demo.show_demo)

dpg.show_viewport()

if (depMode):
   loaded_modules[module_names.index(depModule)].showWindow(show=True)
   dpg.set_primary_window(config["carbon"]["depMode"],True)

dpg.start_dearpygui()
dpg.destroy_context()
exit()