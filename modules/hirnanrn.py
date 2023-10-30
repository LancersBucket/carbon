import sys
sys.path.append('../Carbon')
import carbonmodulehelper as cmh
import dearpygui.dearpygui as dpg
import names

def generateNames():
    for i in range(numNames):
        dpg.set_value("male"+str(i),names.get_full_name('male'))
        dpg.set_value("female"+str(i),names.get_full_name('female'))

# Isn't needed but recomened to be set as the main window's on_close callback
def destroy():
    dpg.delete_item("hirnanrn")
    pass

# CL will search for an init function when the module is loaded, helpful for any preinitalization needed for the module.
def init():
    global config
    global numNames
    config = cmh.readConfig("hirnanrn")
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
        for i in range(numNames):
            dpg.add_text(tag="male"+str(i))
        
        dpg.add_text("\nFemale:")
        for i in range(numNames):
            dpg.add_text(tag="female"+str(i))

        dpg.add_button(label="Regenerate",callback=generateNames)

        generateNames()
    dpg.set_item_pos("hirnanrn",[0,19])