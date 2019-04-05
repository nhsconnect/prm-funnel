---
layout: integration-bar
title:  "GP2GP"
date:   203-20 12:28:00 +0000
timeframe: March 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [ 
    {
      "pathway": "Emis - Emis",
      "Integrated": 94907,
      "NotIntegrated": 15427,
      "Failure": 2443
    }, {
      "pathway": "TPP - Emis",
      "Integrated": 26575,
      "NotIntegrated": 8666,
      "Failure": 1106
    }, {
      "pathway": "Emis - TPP",
      "Integrated": 24919,
      "NotIntegrated": 5017,
      "Failure": 1614
    }, {
      "pathway": "Emis - Vision",
      "Integrated": 3664,
      "NotIntegrated": 761,
      "Failure": 3114
    }, {
      "pathway": "Unknown - Emis",
      "Integrated": 1727,
      "NotIntegrated": 482,
      "Failure": 53
    }, {
      "pathway": "TPP - Vision",
      "Integrated": 987,
      "NotIntegrated": 340,
      "Failure": 504
    }, {
      "pathway": "Unknown - TPP",
      "Integrated": 457,
      "NotIntegrated": 156,
      "Failure": 31
    }, {
      "pathway": "TPP - Microtest",
      "Integrated": 138,
      "NotIntegrated": 77,
      "Failure": 334
    }, {
      "pathway": "Emis - Microtest",
      "Integrated": 122,
      "NotIntegrated": 33,
      "Failure": 297
    }
    ]
---
A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

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
        SenderSupplier=="INPS", "INPS", SenderSupplier=="Microtest", "Microtest", 
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
