import json

contract = {
    "success": int,
    "failure": int,
}

year = 2019
month = 12

additional = {
    "failure": {
        "name": "Failed",
        "link": "month/{0}-{1}/sr-funnel/success-vs-failure/success-vs-failure".format(year, month)
    },
    "success": {
        "name": "Succeeded"
    }
}

with open("success-vs-failure.json", "r") as read_file:
    data = json.load(read_file)

result = []

line = data["result"]

for key in contract.keys():
    newLine = {}
    newLine["name"] = additional[key]["name"]
    newLine["value"] = contract[key](line[key])
    if "link" in additional[key]:
        newLine["link"] = additional[key]["link"]
    result.append(newLine)

print(json.dumps(result, indent=2))
