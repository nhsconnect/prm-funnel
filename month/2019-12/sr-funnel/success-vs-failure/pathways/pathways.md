---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-12-12 14:10:00 +0000"
timeframe: December 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
 {
    "pathway": "EMIS-EMIS",
    "success": 97905,
    "failure": 545,
    "Total": 98450
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 143,
    "failure": 125,
    "Total": 268
  },
  {
    "pathway": "EMIS-TPP",
    "success": 31947,
    "failure": 236,
    "Total": 32183
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 29,
    "Total": 29
  },
  {
    "pathway": "EMIS-Vision",
    "success": 2153,
    "failure": 1175,
    "Total": 3328
  },
  {
    "pathway": "TPP-EMIS",
    "success": 26973,
    "failure": 878,
    "Total": 27851
  },
  {
    "pathway": "TPP-Microtest",
    "success": 39,
    "failure": 186,
    "Total": 225
  },
  {
    "pathway": "TPP-TPP",
    "success": 0,
    "failure": 3,
    "Total": 3
  },
  {
    "pathway": "TPP-Vision",
    "success": 191,
    "failure": 701,
    "Total": 892
  },
  {
    "pathway": "Unknown",
    "success": 159351,
    "failure": 3878,
    "Total": 163229
  }
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st December 2019**:

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
