---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-11-01 14:09:00 +0000"
timeframe: September 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 168987,
    "failure": 883,
    "Total": 169870
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 361,
    "failure": 264,
    "Total": 625
  },
  {
    "pathway": "EMIS-TPP",
    "success": 53423,
    "failure": 360,
    "Total": 53783
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 48,
    "Total": 48
  },
  {
    "pathway": "EMIS-Vision",
    "success": 4365,
    "failure": 2081,
    "Total": 6446
  },
  {
    "pathway": "TPP-EMIS",
    "success":55638,
    "failure": 1164,
    "Total": 56802
  },
  {
    "pathway": "TPP-Microtest",
    "success": 102,
    "failure": 393,
    "Total": 495
  },
  {
    "pathway": "TPP-TPP",
    "success": 1,
    "failure": 2,
    "Total": 3
  },  
  {
    "pathway": "TPP-Vision",
    "success": 439,
    "failure": 1553,
    "Total": 1992
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 24,
    "failure": 0,
    "Total": 24
  },
  {
    "pathway": "Unknown-Vision",
    "success": 0,
    "failure": 3,
    "Total": 3
  }  
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th September 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
      | rename RequestorODS as SenderODS
      | rename RequestorSoftware as SenderSoftware]
  | rex field=SenderSoftware "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
  | eval SenderSupplier=coalesce(SenderSupplier, "Unknown")
  | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
  | rex field=RequestorSoftware "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
  | lookup Spine2-NACS-Lookup NACS AS RequestorODS OUTPUTNEW MName AS MName
  | eval RequestorSupplier=coalesce(RequestorSupplier, MName, "Unknown")
  | eval RequestorSupplier=case(
      RequestorSupplier=="EMIS", "EMIS",
      RequestorSupplier=="TPP", "TPP",
      RequestorSupplier=="INPS", "Vision",
      RequestorSupplier=="Microtest", "Microtest",
      1=1, "Unknown")
  | eval ExtractFailurePoint=coalesce(ExtractFailurePoint, -1)
  | eval RequestAckCode=coalesce(RequestAckCode, -1)
  | eval RequestAckCode=tonumber(RequestAckCode)
  | eval is_success=if(ExtractFailurePoint==0 and RequestAckCode==0,1,0)
  | eval is_failure=if(is_success==1,0,1)
  | eval pathway=SenderSupplier + "-" + RequestorSupplier
  | dedup ConversationID
  | stats sum(is_success) as success,
          sum(is_failure) as failure
    by pathway
  | addcoltotals
  | addtotals
```
