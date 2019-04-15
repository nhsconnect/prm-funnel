---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-03-20 12:28:00 +0000"
timeframe: March 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 112322,
    "failure": 526,
    "Total": 112848
  },
  {
    "pathway": "EMIS-TPP",
    "success": 34011,
    "failure": 203,
    "Total": 34214
  },
  {
    "pathway": "TPP-EMIS",
    "success": 32110,
    "failure": 1439,
    "Total": 33549
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 5529,
    "failure": 44,
    "Total": 5573
  },
  {
    "pathway": "EMIS-Vision",
    "success": 3617,
    "failure": 1723,
    "Total": 5340
  },
  {
    "pathway": "Unknown-TPP",
    "success": 1704,
    "failure": 12,
    "Total": 1716
  },
  {
    "pathway": "TPP-Vision",
    "success": 400,
    "failure": 1083,
    "Total": 1483
  },
  {
    "pathway": "TPP-Microtest",
    "success": 83,
    "failure": 423,
    "Total": 506
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 325,
    "failure": 179,
    "Total": 504
  },
  {
    "pathway": "Unknown-Vision",
    "success": 127,
    "failure": 77,
    "Total": 204
  }
]

---
A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

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
