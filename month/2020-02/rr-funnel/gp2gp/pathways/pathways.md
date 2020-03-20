---
layout: integration-bar
title: "GP2GP Pathways"
date: "2020-02-12 14:10:30 +0000"
timeframe: February 2020
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    {
      "pathway": "EMIS-EMIS",
      "integrated_count": 105987,
      "not_integrated_count": 12138,
      "error_count": 1588,
      "Total": 119713,
    },
    {
      "pathway": "EMIS-Microtest",
      "integrated_count": 66,
      "not_integrated_count": 16,
      "error_count": 201,
      "Total": 283,
    },
    {
      "pathway": "EMIS-TPP",
      "integrated_count": 26013,
      "not_integrated_count": 4866,
      "error_count": 1201,
      "Total": 32080,
    },
    {
      "pathway": "EMIS-Unknown",
      "integrated_count": 0,
      "not_integrated_count": 0,
      "error_count": 1,
      "Total": 1,
    },
    {
      "pathway": "EMIS-Vision",
      "integrated_count": 2536,
      "not_integrated_count": 322,
      "error_count": 1643,
      "Total": 4501,
    },
    {
      "pathway": "TPP-EMIS",
      "integrated_count": 25805,
      "not_integrated_count": 7985,
      "error_count": 990,
      "Total": 34780,
    },
    {
      "pathway": "TPP-Microtest",
      "integrated_count": 51,
      "not_integrated_count": 8,
      "error_count": 137,
      "Total": 196,
    },
    {
      "pathway": "TPP-TPP",
      "integrated_count": 7,
      "not_integrated_count": 0,
      "error_count": 34,
      "Total": 41,
    },
    {
      "pathway": "TPP-Unknown",
      "integrated_count": 0,
      "not_integrated_count": 0,
      "error_count": 0,
      "Total": 0,
    },
    {
      "pathway": "TPP-Vision",
      "integrated_count": 667,
      "not_integrated_count": 196,
      "error_count": 417,
      "Total": 1280,
    },
  ]
---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-29th February 2020**:

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
