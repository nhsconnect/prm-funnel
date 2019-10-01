---
layout: integration-bar
title:  "GP2GP Pathways"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "integrated_count": <EMIS-EMIS:integrated_count>,
    "not_integrated_count": <EMIS-EMIS:not_integrated_count>,
    "error_count": <EMIS-EMIS:error_count>,
    "Total": <EMIS-EMIS:Total>
  },
  {
    "pathway": "EMIS-TPP",
    "integrated_count": <EMIS-TPP:integrated_count>,
    "not_integrated_count": <EMIS-TPP:not_integrated_count>,
    "error_count": <EMIS-TPP:error_count>,
    "Total": <EMIS-TPP:Total>
  },
  {
    "pathway": "TPP-EMIS",
    "integrated_count": <TPP-EMIS:integrated_count>,
    "not_integrated_count": <TPP-EMIS:not_integrated_count>,
    "error_count": <TPP-EMIS:error_count>,
    "Total": <TPP-EMIS:Total>
  },
  {
    "pathway": "EMIS-Vision",
    "integrated_count": <EMIS-Vision:integrated_count>,
    "not_integrated_count": <EMIS-Vision:not_integrated_count>,
    "error_count": <EMIS-Vision:error_count>,
    "Total": <EMIS-Vision:Total>
  },
  {
    "pathway": "TPP-Vision",
    "integrated_count": <TPP-Vision:integrated_count>,
    "not_integrated_count": <TPP-Vision:not_integrated_count>,
    "error_count": <TPP-Vision:error_count>,
    "Total": <TPP-Vision:Total>
  },
  {
    "pathway": "EMIS-Microtest",
    "integrated_count": <EMIS-Microtest:integrated_count>,
    "not_integrated_count": <EMIS-Microtest:not_integrated_count>,
    "error_count": <EMIS-Microtest:error_count>,
    "Total": <EMIS-Microtest:Total>
  },
  {
    "pathway": "TPP-Microtest",
    "integrated_count": <TPP-Microtest:integrated_count>,
    "not_integrated_count": <TPP-Microtest:not_integrated_count>,
    "error_count": <TPP-Microtest:error_count>,
    "Total": <TPP-Microtest:Total>
  },
  {
    "pathway": "TPP-TPP",
    "integrated_count": <TPP-TPP:integrated_count>,
    "not_integrated_count": <TPP-TPP:not_integrated_count>,
    "error_count": <TPP-TPP:error_count>,
    "Total": <TPP-TPP:Total>
  }
]

---

A chart representing the details of GP2GP failures.

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

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
