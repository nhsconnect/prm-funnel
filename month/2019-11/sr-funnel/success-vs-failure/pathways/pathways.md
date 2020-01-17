---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-12-02 14:10:00 +0000"
timeframe: November 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 126156,
    "failure": 708,
    "Total": 126864
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 201,
    "failure": 192,
    "Total": 393
  },
  {
    "pathway": "EMIS-TPP",
    "success": 41781,
    "failure": 243,
    "Total": 42024
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 36,
    "Total": 36
  },
  {
    "pathway": "EMIS-Vision",
    "success": 3020,
    "failure": 1561,
    "Total": 4581
  },
  {
    "pathway": "TPP-EMIS",
    "success": 34631,
    "failure": 900,
    "Total": 35531
  },
  {
    "pathway": "TPP-Microtest",
    "success": 54,
    "failure": 236,
    "Total": 290
  },
  {
    "pathway": "TPP-TPP",
    "success": 2,
    "failure": 14,
    "Total": 16
  },
  {
    "pathway": "TPP-Vision",
    "success": 239,
    "failure": 904,
    "Total": 1143
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 17,
    "failure": 0,
    "Total": 17
  }
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th November 2019**:

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
