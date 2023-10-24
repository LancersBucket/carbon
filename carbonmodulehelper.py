import json

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