import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import carbonmodulehelper as cmh
import importlib

config = cmh.readConfig("global")

dpg.create_context()
dpg.create_viewport(title='Carbon', width=700, height=600)
dpg.setup_dearpygui()

# Module Loader
def dynamicModuleImport(module_name):
   try:
      load_module = importlib.import_module(module_name)
   except Exception as e:
      print("[CL] Error: "+str(e))
      return (False, None)
   try:
      load_module.init()
   except:
      print("[CL] Warning: Module \'" + module_name + "\' does not have an init function")
   return (True, load_module)

# Generates an array of module data and human names
loaded_modules = []
module_names = []
for module in config["modules"]:
   out = dynamicModuleImport(module)
   if (out[0]):
      loaded_modules.append(out[1])
      module_names.append(module)

# Handles the regeneration of windows
def window_handler():
   loaded_modules[module_names.index(dpg.get_value("Modules"))].showWindow(show=True)

# Main Carbon Loader Window. Helps open apps.
with dpg.window(label="Carbon Loader",tag="CL",show=True,no_open_over_existing_popup=False,width=200,height=300,on_close=dpg.delete_item("CL"),no_close=True):
   dpg.add_text("Carbon")
   dpg.add_listbox(module_names,tag="Modules",callback=window_handler)

def showCarbonLoader(sender):
   dpg.focus_item("CL")

def showDemo():
   demo.show_demo()

with dpg.viewport_menu_bar():
   dpg.add_menu_item(label="Carbon Loader", tag="Carbon Loader", callback=showCarbonLoader)
   dpg.add_menu_item(label="Demo Menu", tag="Demo Menu", callback=showDemo)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
quit()