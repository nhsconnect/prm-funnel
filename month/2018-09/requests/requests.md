---
layout: chart
title:  "EHR Requests"
date: "2019-03-20 12:28:00 +0000"
funnel_slice: EHR Requests Sent
timeframe: Sep 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 150107
  },
  {
    "name": "TPP -> EMIS",
    "value": 54806
  },
  {
    "name": "EMIS -> TPP",
    "value": 52371
  },
  {
    "name": "Vision -> EMIS",
    "value": 8541
  },
  {
    "name": "Vision -> TPP",
    "value": 2919
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 757
  },
  {
    "name": "MicroTest -> TPP",
    "value": 690
  },
  {
    "name": "TPP -> TPP",
    "value": 349
  },
  {
    "name": "EMIS -> unknown",
    "value": 6
  }
]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-30th September 2018:

```sql
 index="gp2gp-mi" sourcetype="gppractice-RR"
    | where RequestFailurePoint=0 OR RequestFailurePoint=60 
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
