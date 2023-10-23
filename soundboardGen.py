import json, os

jsonFile = "soundboard.json"

# Prevents the script from overwriting any custom names
if (os.path.isfile(jsonFile)):
    exit()

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

