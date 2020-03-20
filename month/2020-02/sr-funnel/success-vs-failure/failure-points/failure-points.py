import json

contract = {
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
}

year = 2019
month = 11

additional = {
    "gp2_gp_disabled": {
        "name": "GP2GP disabled"        
    },
    "patient_not_at_surgery": {
        "name": "Patient not at surgery	"
    },
    "patient_lookup_failure": {
        "name": "Patient lookup failure"        
    },
    "requestor_not_current_gp": {
        "name": "Requestor not current gp"        
    },
    "comms_setup": {
        "name": "Communications setup failure"
    },
    "not_lm": {
        "name": "Requestor not large message compliant"        
    },
    "lm_problem": {
        "name": "Large message failure"
    },
    "generate_problem": {
        "name": "Unable to generate EHR extract"
    },
    "send_problem": {
        "name": "Unable to send EHR extract"
    },
    "unknown": {
        "name": "Unknown issue"
    }
}

with open("failure-points.json", "r") as read_file:
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