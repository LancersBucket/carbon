# Isn't needed but recomened to be set as the main window's on_close callback
def destroy():
    # Typical use case: dpg.delete_item(windowName)
    pass

# CL will search for an init function when the module is loaded, helpful for any preinitalization needed for the module.
def init():
    pass

# Required: Helper function for CL. This will run when trying to refocus the window through CL.
def focusWindow():
    # dpg.focus_item(windowName)
    pass

# Required: Main window function. This will run when the module is opened.
def showWindow(show=False):
    pass