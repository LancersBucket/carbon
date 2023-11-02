import sys
sys.path.append('../Carbon')
import carbonmodulehelper as cmh
import dearpygui.dearpygui as dpg
import names

def generateNames():
    maleNames = ""
    femaleNames = ""
    for i in range(numNames):
        maleNames += names.get_full_name('male') + "\n\n"
        femaleNames += names.get_full_name('female') + "\n\n"
        
    dpg.set_value("male",maleNames)
    dpg.set_value("female",femaleNames)

# Isn't needed but recomened to be set as the main window's on_close callback
def destroy():
    dpg.delete_item("hirnanrn")
    pass

# CL will search for an init function when the module is loaded, helpful for any preinitalization needed for the module.
def init():
    global config
    global numNames
    config = cmh.getConfig("hirnanrn")
    numNames = cmh.readValue(config,"numNames",5)

# Required: Helper function for CL. This will run when trying to refocus the window through CL.
def focusWindow():
    dpg.focus_item("hirnanrn")
    pass

# Required: Main window function. This will run when the module is opened.
def showWindow(show=False):
    with dpg.window(label="Help! I Really Need A Name Right Now!",tag="hirnanrn",show=show,autosize=True,on_close=destroy):
        #dpg.add_text("Help! I Really Need A Name Right Now!")
        dpg.add_text("Male:")
        dpg.add_text(tag="male")
        
        dpg.add_text("Female:")
        dpg.add_text(tag="female")

        dpg.add_button(label="Regenerate",callback=generateNames)

        generateNames()
    dpg.set_item_pos("hirnanrn",[0,19])