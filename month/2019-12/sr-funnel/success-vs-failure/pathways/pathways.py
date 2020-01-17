import json

{"pathway": "EMIS-EMIS", "success": "126156", "failure": "708", "Total": "126864"}

contract = {
    "pathway": str,
    "success": int,
    "failure": int,
    "Total": int,
}

with open("pathways.json", "r") as read_file:
    data = json.load(read_file)

result = []

for eachItem in data["data"]:
    line = eachItem["result"]
    newLine = {}
    for key in contract.keys():
        try:
            newLine[key] = contract[key](line[key])
        except:
            if key == "pathway":
                newLine["pathway"] = "Unknown"
            else:
                print("failed on key: '{0}'".format(key))
                print(newLine)
                print(line)
    result.append(newLine)

print(json.dumps(result, indent=2))
