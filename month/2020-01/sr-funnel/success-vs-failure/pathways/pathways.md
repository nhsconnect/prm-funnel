---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2020-01-12 14:10:30 +0000"
timeframe: January 2020
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 136777,
    "failure": 697,
    "Total": 137474
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 243,
    "failure": 226,
    "Total": 469
  },
  {
    "pathway": "EMIS-TPP",
    "success": 41705,
    "failure": 270,
    "Total": 41975
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 33,
    "Total": 33
  },
  {
    "pathway": "EMIS-Vision",
    "success": 2955,
    "failure": 1587,
    "Total": 4542
  },
  {
    "pathway": "TPP-EMIS",
    "success": 36717,
    "failure": 1162,
    "Total": 37879
  },
  {
    "pathway": "TPP-Microtest",
    "success": 58,
    "failure": 320,
    "Total": 378
  },
  {
    "pathway": "TPP-TPP",
    "success": 1,
    "failure": 5,
    "Total": 6
  },
  {
    "pathway": "TPP-Vision",
    "success": 222,
    "failure": 994,
    "Total": 1216
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 22,
    "failure": 106,
    "Total": 128
  },
  {
    "pathway": "Unknown-TPP",
    "success": 1,
    "failure": 0,
    "Total": 1
  },
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2020**:

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
