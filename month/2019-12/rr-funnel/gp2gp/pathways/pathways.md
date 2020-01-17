---
layout: integration-bar
title:  "GP2GP Pathways"
date: "2019-12-12 14:10:30 +0000"
timeframe: December 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "integrated_count": 84008,
    "not_integrated_count": 13041,
    "error_count": 1378,
    "Total": 98427
  },
   {
    "pathway": "EMIS-Microtest",
    "integrated_count": 105,
    "not_integrated_count": 29,
    "error_count": 260,
    "Total": 394
  },
   {
    "pathway": "EMIS-TPP",
    "integrated_count": 22085,
    "not_integrated_count": 4960,
    "error_count": 974,
    "Total": 28019
  },
   {
    "pathway": "EMIS-Unknown",
    "integrated_count": 9,
    "not_integrated_count": 0,
    "error_count": 15,
    "Total": 24
  },
   {
    "pathway": "EMIS-Vision",
    "integrated_count": 2154,
    "not_integrated_count": 414,
    "error_count": 1708,
    "Total": 4276
  },
   {
    "pathway": "TPP-EMIS",
    "integrated_count": 22952,
    "not_integrated_count": 8101,
    "error_count": 886,
    "Total": 31939
  },
   {
    "pathway": "TPP-Microtest",
    "integrated_count": 282,
    "not_integrated_count": 78,
    "error_count": 1095,
    "Total": 1455
  },
   {
    "pathway": "TPP-TPP",
    "integrated_count": 1,
    "not_integrated_count": 2,
    "error_count": 18,
    "Total": 21
  },
   {
    "pathway": "TPP-Vision",
    "integrated_count": 568,
    "not_integrated_count": 190,
    "error_count": 405,
    "Total": 1163
  }
]

---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st December 2019**:

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
