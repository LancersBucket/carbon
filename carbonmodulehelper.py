from dearpygui.dearpygui import save_init_file, viewport_menu_bar, add_menu_item, delete_item
import json, os

carbonCore = ["shuffle","soundboard","mythril","hirnanrn"]

def __cmhLogger(msg):
    print("[CMH]: " + str(msg))

# Gets module or global config from json file
def getConfig(moduleName: str) -> dict:
    ConfigData = open("carbonConfig.json")
    Data = json.load(ConfigData)
    if (moduleName != "global"):
        return Data["modules"][moduleName]
    else:
        return Data
    
# Reads a value from the config with error handling built in, in case the key doesn't exist in the config
def readValue(config: dict, configValue: str, failReturn=False):
    try:
        retVal = config[configValue]
    except:
        retVal = failReturn
    return retVal

## TODO, Write function
#def writeConfig(moduleName: str, key, operation, value=None):
#    pass

# Save window states
def save() -> None:
    save_init_file("dpg.ini")

# Returns if a module is part of Carbon Core
def isCarbonCore(moduleName: str) -> bool:
    try:
        carbonCore.index(moduleName)
    except:
        return False
    return True

# Returns a list of Carbon Core modules
def getCarbonCore() -> list[str]:
    return carbonCore

def checkFolder(folderName: str, createFolder: bool = True, listFolder: bool = True) -> list[str]:
    if (not os.path.isdir(folderName)):
        if (not createFolder):
            return None
        else:
            try:
                os.mkdir(folderName)
            except Exception as e:
                __cmhLogger(e)
                return None
            return os.listdir(folderName)
    else:
        if (listFolder):
            return os.listdir(folderName)

def addMenuBarItem(label:str, tag:int|str, callback=None) -> None:
    with viewport_menu_bar():
        add_menu_item(label=label, tag=tag, callback=callback)

def removeMenuBarItem(tag):
    try:
        delete_item(tag)
    except Exception as e:
        __cmhLogger(e)