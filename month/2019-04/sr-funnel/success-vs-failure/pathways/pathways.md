---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "2019-03-20 12:28:00 +0000"
timeframe: April 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": 92219,
    "failure": 526,
    "Total": 92745
  },
  {
    "pathway": "EMIS-TPP",
    "success": 29279,
    "failure": 434,
    "Total": 29713
  },
  {
    "pathway": "TPP-EMIS",
    "success": 32110,
    "failure": 1439,
    "Total": 33549
  },
  {
    "pathway": "Unknown-EMIS",
    "success": 9389,
    "failure": 62,
    "Total": 9451
  },
  {
    "pathway": "EMIS-Vision",
    "success": 4184,
    "failure": 1758,
    "Total": 5942
  },
  {
    "pathway": "Unknown-TPP",
    "success": 2687,
    "failure": 72,
    "Total": 2759
  },
  {
    "pathway": "TPP-Vision",
    "success": 501,
    "failure": 1003,
    "Total": 1504
  },
  {
    "pathway": "TPP-Microtest",
    "success": 84,
    "failure": 351,
    "Total": 435
  },
  {
    "pathway": "EMIS-Microtest",
    "success": 277,
    "failure": 165,
    "Total": 442
  },
  {
    "pathway": "Unknown-Vision",
    "success": 431,
    "failure": 188,
    "Total": 619
  }
]

---
A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th April 2019**:

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
