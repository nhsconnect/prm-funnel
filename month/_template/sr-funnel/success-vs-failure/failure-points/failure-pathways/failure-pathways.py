import json

contract = {
    "pathway":str,
    "gp2_gp_disabled":int,
    "patient_not_at_surgery":int,
    "patient_lookup_failure":int,
    "requestor_not_current_gp":int,
    "comms_setup":int,
    "not_lm":int,
    "lm_problem":int,
    "generate_problem":int,
    "send_problem":int,
    "unknown":int,
    "Total":int
}

with open("failure_pathways.json", "r") as read_file:
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