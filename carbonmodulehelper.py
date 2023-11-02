from dearpygui.dearpygui import save_init_file
import json

carbonCore = ["shuffle","soundboard","mythril","hirnanrn"]

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