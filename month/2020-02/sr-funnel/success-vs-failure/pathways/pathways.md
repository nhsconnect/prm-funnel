---
layout: extract-bar
title: "EHR Extract Pathways"
date: "2020-02-12 14:11:00 +0000"
timeframe: February 2020
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
  "pathway": "EMIS-EMIS",
  "success": 118796,
  "failure": 822,
  "Total": 119618
  },
  {
  "pathway": "EMIS-Microtest",
  "success": 108,
  "failure": 98,
  "Total": 206
  },
  {
  "pathway": "EMIS-TPP",
  "success": 34672,
  "failure": 346,
  "Total": 35018
  },
  {
  "pathway": "EMIS-Unknown",
  "success": 0,
  "failure": 41,
  "Total": 41
  },
  {
  "pathway": "EMIS-Vision",
  "success": 2441,
  "failure": 1322,
  "Total": 3763
  },
  {
  "pathway": "TPP-EMIS",
  "success": 30940,
  "failure": 1084,
  "Total": 32024
  },
  {
  "pathway": "TPP-Microtest",
  "success": 31,
  "failure": 143,
  "Total": 174
  },
  {
  "pathway": "TPP-TPP",
  "success": 2,
  "failure": 17,
  "Total": 19
  },
  {
  "pathway": "TPP-Vision",
  "success": 230,
  "failure": 798,
  "Total": 1028
  },
  {
  "pathway": "Unknown-EMIS",
  "success": 2,
  "failure": 0,
  "Total": 2
  }
]
---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-29th February 2020**:

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
