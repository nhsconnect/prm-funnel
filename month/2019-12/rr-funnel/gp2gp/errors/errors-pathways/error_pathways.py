import json

contract = {
    "pathway":str,
    "unknown_count":int,
    "lm_failure_count":int,
    "tpp_limits_count":int,
    "duplicate_count":int,
    "failed_to_generate_count":int,
    "unknown_patient_count":int,
    "received_and_rejected_count":int,
    "other_count":int,
    "Total":int
}

with open("error_pathways.json", "r") as read_file:
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