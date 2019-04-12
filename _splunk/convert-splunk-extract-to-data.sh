#!/bin/sh

if [ -z "$1" ]; then
  echo "Must specify file"
  echo "Usage: $0 <file>"
  exit 1
fi

cat "$1" | jq -n 'def keyfield: [inputs][0].result | to_entries | .[0].key; [[inputs] | .[] | .result | with_entries(if (.value | test("\\d+")) then {"key":.key, "value":.value|tonumber} else {"key":.key, "value":.value} end)] | sort_by(.Total) | reverse'
