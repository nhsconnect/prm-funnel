---
layout: integration-bar
title:  "GP2GP Pathways"
date: "2020-01-12 14:10:30 +0000"
timeframe: January 2020
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "integrated_count": 118059,
    "not_integrated_count": 18002,
    "error_count": 1630,
    "Total": 137691
  },
  {
    "pathway": "EMIS-Microtest",
    "integrated_count": 95,
    "not_integrated_count": 43,
    "error_count": 294,
    "Total": 432
  },
  {
    "pathway": "EMIS-TPP",
    "integrated_count": 29972,
    "not_integrated_count": 6704,
    "error_count": 1225,
    "Total": 37901
  },
  {
    "pathway": "EMIS-Unknown",
    "integrated_count": 15,
    "not_integrated_count": 0,
    "error_count": 24,
    "Total": 39
  },
  {
    "pathway": "EMIS-Vision",
    "integrated_count": 3179,
    "not_integrated_count": 534,
    "error_count": 1844,
    "Total": 5557
  },
  {
    "pathway": "TPP-EMIS",
    "integrated_count": 30649,
    "not_integrated_count": 9909,
    "error_count": 1165,
    "Total": 41723
  },
  {
    "pathway": "TPP-Microtest",
    "integrated_count": 86,
    "not_integrated_count": 47,
    "error_count": 275,
    "Total": 408
  },
  {
    "pathway": "TPP-TPP",
    "integrated_count": 0,
    "not_integrated_count": 0,
    "error_count": 16,
    "Total": 16
  },
  {
    "pathway": "TPP-Vision",
    "integrated_count": 866,
    "not_integrated_count": 294,
    "error_count": 453,
    "Total": 1613
  },
  {
    "pathway": "Unknown-EMIS",
    "integrated_count": 1,
    "not_integrated_count": 3,
    "error_count": 0,
    "Total": 4
  },
]

---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2020**:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS, "Unknown")
    | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
    | rex field=RequestorSoftware "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
    | eval RequestorSupplier=coalesce(RequestorSupplier, "Unknown")
    | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
    | rename RequestorODS as SenderODS | rename RequestorSoftware as SenderSoftware]
    | rex field=SenderSoftware "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
    | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS SenderMName
    | eval SenderSupplier=coalesce(SenderSupplier, SenderMName, "Unknown")
    | eval SenderSupplier=case(
        SenderSupplier=="EMIS", "EMIS", SenderSupplier=="TPP", "TPP",
        SenderSupplier=="INPS", "Vision", SenderSupplier=="Microtest", "Microtest",
        1=1, "Unknown")
    | eval RegistrationType=coalesce(RegistrationType,0)
    | eval RequestFailureType=coalesce(RequestFailureType,-1)
    | eval RequestFailurePoint=coalesce(RequestFailurePoint,-1)
    | eval RequestErrorCode=tonumber(coalesce(RequestErrorCode,-1))
    | eval ExtractAckCode=tonumber(coalesce(ExtractAckCode,-1))
    | eval ExtractEventTime=coalesce(ExtractAckTime,ExtractTime)
    | eval ExtractResult=if(ExtractAckCode==-1 and isnotnull(ExtractEventTime),0,ExtractAckCode)
    | eval category=case(
        RequestFailurePoint==0 and RequestErrorCode==-1 and
        (ExtractResult==0 or ExtractResult==15) and
        ((ExtractAckStatus==1 and ExtractAckCode==0) or
        (ExtractAckStatus==5 and ExtractAckCode==15)),"GP2GP Success and Integrated",
        RequestFailurePoint==0 and RequestErrorCode==-1 and
        (ExtractResult==0 or ExtractResult==15),"GP2GP Success not Integrated",
        (RegistrationType!=3 and RequestFailureType!=2 and
        RequestFailureType!=5 and RequestFailurePoint==60) or
        (RequestFailurePoint==0 and isnull(RequestFailureTime) and
        (RequestErrorCode!=-1 or (ExtractResult!=0 and
        ExtractResult!=15))),"GP2GP Failure")
    | eval is_integrated=if(category=="GP2GP Success and Integrated",1,0)
    | eval is_not_integrated=if(category=="GP2GP Success not Integrated",1,0)
    | eval is_error=if(category=="GP2GP Failure",1,0)
    | eval pathway=RequestorSupplier + "-" + SenderSupplier
    | dedup key
    | stats sum(is_integrated) as integrated_count,
        sum(is_not_integrated) as not_integrated_count,
        sum(is_error) as error_count by pathway
    | addcoltotals
    | addtotals
```
