---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-10-02 09:13:12"
timeframe: August 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 127425,
    "failure": 568,
    "Total": 127993
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 263,
    "failure": 189,
    "Total": 452
  },
  {
    "pathway": "EMIS-TPP",
    "success": 40074,
    "failure": 207,
    "Total": 40281
  },
  {
    "pathway": "EMIS-Unknown",
    "success": 0,
    "failure": 5,
    "Total": 5
  },
  {
    "pathway": "EMIS-Vision",
    "success": 3388,
    "failure": 1781,
    "Total": 5169
  },
  {
    "pathway": "TPP-EMIS",
    "success": 34108,
    "failure": 894,
    "Total": 35002
  },
  {
    "pathway": "TPP-Microtest",
    "success": 52,
    "failure": 298,
    "Total": 350
  },
  {
    "pathway": "TPP-TPP",
    "success": 2,
    "failure": 2,
    "Total": 4
  },
  {
    "pathway": "TPP-Vision",
    "success": 306,
    "failure": 996,
    "Total": 1302
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 1,
    "failure": 0,
    "Total": 1
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

The data was collected from **Splunk** with the following query, and the date range was **1st-31st August 2019**:

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
