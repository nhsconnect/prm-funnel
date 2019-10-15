---
layout: integration-bar
title:  "GP2GP Pathways"
date: "2019-10-01 14:10:00 +0000"
timeframe: July 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "integrated_count": 118727,
    "not_integrated_count": 9512,
    "error_count": 2557,
    "Total": 130796
  },
  {
    "pathway": "EMIS-Microtest",
    "integrated_count": 123,
    "not_integrated_count": 21,
    "error_count": 318,
    "Total": 462
  },
  {
    "pathway": "EMIS-TPP",
    "integrated_count": 29863,
    "not_integrated_count": 3292,
    "error_count": 1105,
    "Total": 34260
  },
  {
    "pathway": "EMIS-Unknown",
    "integrated_count": 0,
    "not_integrated_count": 0,
    "error_count": 2,
    "Total": 2
  },
  {
    "pathway": "EMIS-Vision",
    "integrated_count": 3193,
    "not_integrated_count": 320,
    "error_count": 1895,
    "Total": 5408
  },
  {
    "pathway": "TPP-EMIS",
    "integrated_count": 30068,
    "not_integrated_count": 8910,
    "error_count": 1264,
    "Total": 40242
  },
  {
    "pathway": "TPP-Microtest",
    "integrated_count": 111,
    "not_integrated_count": 45,
    "error_count": 261,
    "Total": 417
  },
  {
    "pathway": "TPP-TPP",
    "integrated_count": 0,
    "not_integrated_count": 0,
    "error_count": 17,
    "Total": 17
  },
  {
    "pathway": "TPP-Unknown",
    "integrated_count": 0,
    "not_integrated_count": 0,
    "error_count": 0,
    "Total": 0
  },
  {
    "pathway": "TPP-Vision",
    "integrated_count": 909,
    "not_integrated_count": 331,
    "error_count": 598,
    "Total": 1838
  },
]

---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st July 2019**:

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
