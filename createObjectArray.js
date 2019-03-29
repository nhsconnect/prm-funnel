var labels = [
  "0: Success",
  "99: Unexpected condition"
]

var values = [
  1342,
  2
]

var result = [];
labels.forEach((label, i) => {
    var obj = {}
    obj["name"] = label
    obj["value"] = values[i]
    result.push(obj)
});
console.log(result);