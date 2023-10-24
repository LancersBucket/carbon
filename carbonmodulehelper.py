import json

def readConfig(moduleName):
    ConfigData = open("carbonConfig.json")
    Data = json.load(ConfigData)
    if (moduleName != "global"):
        return Data["modules"][moduleName]
    else:
        return Data

def writeConfig(moduleName, key, operation, value=None):
    pass