---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-11-02 14:10:00 +0000"
timeframe: October 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 160759,
    "failure": 992,
    "Total": 161751
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 316,
    "failure": 258,
    "Total": 574
  },
  {
    "pathway": "EMIS-TPP",
    "success": 52499,
    "failure": 399,
    "Total": 52898
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 12,
    "Total": 12
  },
  {
    "pathway": "EMIS-Vision",
    "success": 3640,
    "failure": 1702,
    "Total": 5342
  },
  {
    "pathway": "TPP-EMIS",
    "success": 48376,
    "failure": 1116,
    "Total": 49492
  },
  {
    "pathway": "TPP-Microtest",
    "success": 63,
    "failure": 293,
    "Total": 356
  },
  {
    "pathway": "TPP-TPP",
    "success": 59,
    "failure": 6,
    "Total": 65
  },
  {
    "pathway": "TPP-Vision",
    "success": 368,
    "failure": 1176,
    "Total": 1544
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 15,
    "failure": 0,
    "Total": 15
  },
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st October 2019**:

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
