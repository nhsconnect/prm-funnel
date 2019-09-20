---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-09-20 12:28:00 +0000"
timeframe: May 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 111348,
    "failure": 646,
    "Total": 111994
  },
  {
    "pathway": "EMIS-TPP",
    "success": 34758,
    "failure": 259,
    "Total": 35017
  },
  {
    "pathway": "TPP-EMIS",
    "success": 30681,
    "failure": 936,
    "Total": 31617
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 32,
    "failure": 1,
    "Total": 33
  },
  {
    "pathway": "EMIS-Vision",
    "success": 3289,
    "failure": 1780,
    "Total": 5069
  },
  {
    "pathway": "Unknown-TPP",
    "success": 0,
    "failure": 0,
    "Total": 0
  },
  {
    "pathway": "TPP-Vision",
    "success": 292,
    "failure": 1036,
    "Total": 1328
  },
  {
    "pathway": "TPP-Microtest",
    "success": 72,
    "failure": 346,
    "Total": 418
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 249,
    "failure": 217,
    "Total": 466
  },
  {
    "pathway": "Unknown-Vision",
    "success": 0,
    "failure": 0,
    "Total": 0
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 160,
    "Total": 160
  }
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st May 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
      | rename RequestorODS as SenderODS
      | rename RequestorSoftware as SenderSoftware]
  | rex field=SenderSoftware "(?&lt;SenderSupplier>.*)_(?&lt;SenderSystem>.*)_(?&lt;SenderVersion>.*)"
  | eval SenderSupplier=coalesce(SenderSupplier, "Unknown")
  | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
  | rex field=RequestorSoftware "(?&lt;RequestorSupplier>.*)_(?&lt;RequestorSystem>.*)_(?&lt;RequestorVersion>.*)"
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
