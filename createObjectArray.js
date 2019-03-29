var labels =[
  "EMIS -> EMIS",
  "EMIS -> TPP",
  "TPP -> EMIS",
  "Vision -> EMIS",
  "Vision -> TPP",
  "MicroTest -> TPP",
  "MicroTest -> EMIS",
  "TPP -> TPP"
]

var values = [
  90095,
  30455,
  26843,
  5448,
  1634,
  413,
  387,
  48
]

var result = [];
labels.forEach((label, i) => {
    var obj = {}
    obj["name"] = label
    obj["value"] = values[i]
    result.push(obj)
});
result = JSON.stringify(result, null, 2);
var proc = require('child_process').spawn('pbcopy'); 
proc.stdin.write("items: " + result); proc.stdin.end();