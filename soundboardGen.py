import json, os

jsonFile = "soundboard.json"

dictionary = {
    "buttons": []
    }

counter = 0
for f in os.listdir("files"):
    dictionary["buttons"].append({"id":counter,"label":f.split("[")[0],"file":f})
    counter += 1


json_object = json.dumps(dictionary, indent=4)


with open(jsonFile, "w") as out:
    out.write(json_object)

