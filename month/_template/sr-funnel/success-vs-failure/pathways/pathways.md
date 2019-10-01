---
layout: extract-bar
title:  "EHR Extract Pathways"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "success": <EMIS-EMIS:Success>,
    "failure": <EMIS-EMIS:Failure>,
    "Total": <EMIS-EMIS:Total>
  },
  {
    "pathway": "EMIS-TPP",
    "success": <EMIS-TPP:Success>,
    "failure": <EMIS-TPP:Failure>,
    "Total": <EMIS-TPP:Total>
  },
  {
    "pathway": "TPP-EMIS",
    "success": <TPP-EMIS:Success>,
    "failure": <TPP-EMIS:Failure>,
    "Total": <TPP-EMIS:Total>
  },
  {
    "pathway": "Unknown-EMIS",
    "success": <Unknown-EMIS:Success>,
    "failure": <Unknown-EMIS:Failure>,
    "Total": <Unknown-EMIS:Total>
  },
  {
    "pathway": "EMIS-Vision",
    "success": <EMIS-Vision:Success>,
    "failure": <EMIS-Vision:Failure>,
    "Total": <EMIS-Vision:Total>
  },
  {
    "pathway": "Unknown-TPP",
    "success": <Unknown-TPP:Success>,
    "failure": <Unknown-TPP:Failure>,
    "Total": <Unknown-TPP:Total>
  },
  {
    "pathway": "TPP-Vision",
    "success": <TPP-Vision:Success>,
    "failure": <TPP-Vision:Failure>,
    "Total": <TPP-Vision:Total>
  },
  {
    "pathway": "TPP-Microtest",
    "success": <TPP-Microtest:Success>,
    "failure": <TPP-Microtest:Failure>,
    "Total": <TPP-Microtest:Total>
  },
  {
    "pathway": "EMIS-Microtest",
    "success": <EMIS-Microtest:Success>,
    "failure": <EMIS-Microtest:Failure>,
    "Total": <EMIS-Microtest:Total>
  },
  {
    "pathway": "Unknown-Vision",
    "success": <Unknown-Vision:Success>,
    "failure": <Unknown-Vision:Failure>,
    "Total": <Unknown-Vision:Total>
  },
  {
    "pathway": "EMIS-Unknown",
    "success": <EMIS-Unknown:Success>,
    "failure": <EMIS-Unknown:Failure>,
    "Total": <EMIS-Unknown:Total>
  }
]

---

A chart representing the details EHR extract success by pathway.

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

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
