import dearpygui.dearpygui as dpg
import json

carbonCore = ["shuffle","soundboard","mythril"]

def readConfig(moduleName: str) -> dict:
    ConfigData = open("carbonConfig.json")
    Data = json.load(ConfigData)
    if (moduleName != "global"):
        return Data["modules"][moduleName]
    else:
        return Data

## TODO, Write function
def writeConfig(moduleName: str, key, operation, value=None):
    pass

# Save window states
def save() -> None:
    dpg.save_init_file("dpg.ini")

def isCarbonCore(moduleName: str) -> bool:
    try:
        carbonCore.index(moduleName)
    except:
        return False
    return True

def getCarbonCore() -> list[str]:
    return carbonCore