---
layout: filing-bar
title:  "Filing By Requester"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: Integrations
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "RequestorSupplier": "EMIS",
    "not_acknowledged_count": <EMIS:not_acknowledged_count>,
    "not_sent_count": <EMIS:not_sent_count>,
    "integrated_count": <EMIS:integrated_count>,
    "rejected_count": <EMIS:rejected_count>,
    "duplicate_count": <EMIS:duplicate_count>,
    "suppressed_count": <EMIS:suppressed_count>,
    "filing_failed_count": <EMIS:filing_failed_count>,
    "other_count": <EMIS:other_count>,
    "Total": <EMIS:Total>
  },
  {
    "RequestorSupplier": "TPP",
    "not_acknowledged_count": <TPP:not_acknowledged_count>,
    "not_sent_count": <TPP:not_sent_count>,
    "integrated_count": <TPP:integrated_count>,
    "rejected_count": <TPP:rejected_count>,
    "duplicate_count": <TPP:duplicate_count>,
    "suppressed_count": <TPP:suppressed_count>,
    "filing_failed_count": <TPP:filing_failed_count>,
    "other_count": <TPP:other_count>,
    "Total": <TPP:Total>
  },
  {
    "RequestorSupplier": "Unknown",
    "not_acknowledged_count": <Unknown:not_acknowledged_count>,
    "not_sent_count": <Unknown:not_sent_count>,
    "integrated_count": <Unknown:integrated_count>,
    "rejected_count": <Unknown:rejected_count>,
    "duplicate_count": <Unknown:duplicate_count>,
    "suppressed_count": <Unknown:suppressed_count>,
    "filing_failed_count": <Unknown:filing_failed_count>,
    "other_count": <Unknown:other_count>,
    "Total": <Unknown:Total>
  }
]
---

A chart representing the filing details.

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS,"Unknown")
    | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
    | rex field=RequestorSoftware "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
    | eval RequestorSupplier=coalesce(RequestorSupplier, RequestorSupplier, "Unknown")
    | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
    | rename RequestorODS as SenderODS
    | rename RequestorSoftware as SenderSoftware]
    | rex field=SenderSoftware "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
    | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName
    | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "Unknown")
    | eval SenderSupplier=case(
        SenderSupplier=="EMIS", "EMIS", SenderSupplier=="TPP", "TPP",
        SenderSupplier=="INPS", "Vision", SenderSupplier=="Microtest", "Microtest",
        1=1, "Unknown")
    | eval RegistrationType=coalesce(RegistrationType,0)
    | eval RequestFailureType=coalesce(RequestFailureType,-1)
    | eval RequestFailurePoint=coalesce(RequestFailurePoint,-1)
    | eval ExtractAckStatus=tonumber(coalesce(ExtractAckStatus,-1))
    | eval ExtractAckCode=tonumber(coalesce(ExtractAckCode,-1))
    | eval ExtractEventTime=coalesce(ExtractAckTime,ExtractTime)
    | eval ExtractResult=if(ExtractAckCode==-1 and isnotnull(ExtractEventTime),0,ExtractAckCode)
    | eval ExtractResultLabel=if(ExtractResult==0,"NONE",ExtractResult)
    | eval ExtractAckStatusLabel=case(
        ExtractAckStatus==-1,"Not acknowledged",
        ExtractAckStatus==0,"Not sent",
        ExtractAckStatus==1 and ExtractResultLabel=="NONE","Integrated",
        ExtractAckStatus==2,"Filing rejected",
        ExtractAckStatus==3,"Duplicate",
        ExtractAckStatus==5,"Suppressed",
        ExtractAckStatus==7,"Filing failed",
        1=1,"Other")
    | where (RequestFailurePoint==0 and isnull(RequestFailureTime)) or
        (RegistrationType!=3 and RequestFailureType!=2 and
        RequestFailureType!=5 and RequestFailurePoint==60)
    | eval is_not_acknowledged=if(ExtractAckStatusLabel=="Not acknowledged",1,0)
    | eval is_not_sent=if(ExtractAckStatusLabel=="Not sent",1,0)
    | eval is_integrated=if(ExtractAckStatusLabel=="Integrated",1,0)
    | eval is_rejected=if(ExtractAckStatusLabel=="Filing rejected",1,0)
    | eval is_duplicate=if(ExtractAckStatusLabel=="Duplicate",1,0)
    | eval is_suppressed=if(ExtractAckStatusLabel=="Suppressed",1,0)
    | eval is_failed=if(ExtractAckStatusLabel=="Filing failed",1,0)
    | eval is_other=if(ExtractAckStatusLabel=="Other",1,0)
    | dedup key
    | stats sum(is_not_acknowledged) as not_acknowledged_count,
        sum(is_not_sent) as not_sent_count,
        sum(is_integrated) as integrated_count,
        sum(is_rejected) as rejected_count,
        sum(is_duplicate) as duplicate_count,
        sum(is_suppressed) as suppressed_count,
        sum(is_failed) as filing_failed_count,
        sum(is_other) as other_count by RequestorSupplier
    | addcoltotals
    | addtotals
```
