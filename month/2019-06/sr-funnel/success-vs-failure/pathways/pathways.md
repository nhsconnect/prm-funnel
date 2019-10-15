---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-09-25 09:13:12"
timeframe: June 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
    {
      "pathway": "EMIS-EMIS",
      "success": 107859,
      "failure": 696,
      "Total": 108555
    },
    {
      "pathway": "EMIS-Microtest",
      "success": 232,
      "failure": 155,
      "Total": 387
    },
    {
      "pathway": "EMIS-TPP",
      "success": 34718,
      "failure": 216,
      "Total": 34934
    },
    {
      "pathway": "EMIS-Unknown",
      "success": 0,
      "failure": 20,
      "Total": 20
    },
    {
      "pathway": "EMIS-Vision",
      "success": 3217,
      "failure": 1767,
      "Total": 4984
    },
    {
      "pathway": "TPP-EMIS",
      "success": 30811,
      "failure": 783,
      "Total": 31594
    },
    {
      "pathway": "TPP-Microtest",
      "success": 75,
      "failure": 300,
      "Total": 375
    },
    {
      "pathway": "TPP-TPP",
      "success": 68,
      "failure": 8,
      "Total": 76
    },
    {
      "pathway": "TPP-Vision",
      "success": 264,
      "failure": 897,
      "Total": 1161
    },
    {
      "pathway": "Unknown-EMIS",
      "success": 23,
      "failure": 1,
      "Total": 24
    },
    {
      "pathway": "Unknown-Vision",
      "success": 0,
      "failure": 1,
      "Total": 1
    }
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th June 2019**:

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
