---
layout: chart
title:  "Integrations"
date: "2019-03-20 15:46:00 +0000"
funnel_slice: Successfully Integrated
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 104811
  },
  {
    "name": "TPP -> EMIS",
    "value": 28367
  },
  {
    "name": "EMIS -> TPP",
    "value": 26521
  },
  {
    "name": "Vision -> EMIS",
    "value": 3874
  },
  {
    "name": "Vision -> TPP",
    "value": 1024
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 139
  },
  {
    "name": "MicroTest -> TPP",
    "value": 123
  }
]
---
A chart representing the successful integrations split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was the whole of February 2019:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | where RequestFailurePoint=0 OR RequestFailurePoint=60 
    | where ExtractAckCode=0 OR ExtractAckCode=00
    | where ExtractAckStatus=1
    | join type=outer RequestorODS 
      [search index="gp2gp-mi" sourcetype="gppractice-HR"] 
    | join type=outer SenderODS 
        [search index="gp2gp-mi" sourcetype="gppractice-HR" 
          | rename RequestorODS as SenderODS 
          | rename RequestorSoftware as SenderSoftware]
    | rex field=RequestorSoftware 
      "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
    | eval RequestorSupplier=coalesce(RequestorSupplier, RequestorSupplier, "unknown")
    | rex field=SenderSoftware 
      "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
    | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName
    | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "unknown")
    | stats dc(ConversationID) as count by SenderSupplier, RequestorSupplier
    | sort - count
```
