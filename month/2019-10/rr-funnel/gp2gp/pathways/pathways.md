---
layout: integration-bar
title: "GP2GP Pathways"
date: "2019-11-02 14:10:00 +0000"
timeframe: October 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "pathway": "EMIS-EMIS",
    "integrated_count": 143511,
    "not_integrated_count": 16190,
    "error_count": 2183,
    "Total": 161884,
  },
  {
    "pathway": "EMIS-Microtest",
    "integrated_count": 179,
    "not_integrated_count": 41,
    "error_count": 375,
    "Total": 595,
  },
  {
    "pathway": "EMIS-TPP",
    "integrated_count": 41804,
    "not_integrated_count": 6426,
    "error_count": 1314,
    "Total": 49544,
  },
  {
    "pathway": "EMIS-Vision",
    "integrated_count": 3640,
    "not_integrated_count": 458,
    "error_count": 2063,
    "Total": 6161,
  },
  {
    "pathway": "TPP-EMIS",
    "integrated_count": 38145,
    "not_integrated_count": 13020,
    "error_count": 1392,
    "Total": 52557,
  },
  {
    "pathway": "TPP-Microtest",
    "integrated_count": 141,
    "not_integrated_count": 60,
    "error_count": 348,
    "Total": 549,
  },
  {
    "pathway": "TPP-TPP",
    "integrated_count": 30,
    "not_integrated_count": 29,
    "error_count": 32,
    "Total": 91,
  },
  {
    "pathway": "TPP-Vision",
    "integrated_count": 1022,
    "not_integrated_count": 322,
    "error_count": 626,
    "Total": 1970,
  },
]

---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st October 2019**:

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
