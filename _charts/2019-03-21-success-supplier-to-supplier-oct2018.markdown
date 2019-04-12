---
layout: chart
title:  "Successful integrations grouped by sending and receiving system type"
date: "2019-03-20 15:46:00 +0000"
funnel_slice: Successfully Integrated
timeframe: Oct 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 140814
  },
  {
    "name": "TPP -> EMIS",
    "value": 42981
  },
  {
    "name": "EMIS -> TPP",
    "value": 38954
  },
  {
    "name": "Vision -> EMIS",
    "value": 5210
  },
  {
    "name": "Vision -> TPP",
    "value": 1536
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 232
  },
  {
    "name": "MicroTest -> TPP",
    "value": 157
  },
  {
    "name": "TPP -> TPP",
    "value": 38
  },
  {
    "name": "EMIS -> Unknown",
    "value": 6
  }
]
---
A chart representing the successful integrations split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was the whole of October 2018:

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
