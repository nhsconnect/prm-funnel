---
layout: chart
title: "GP2GP Details"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    {
      name: "Integrated",
      value: <GP2GP Success and Integrated>,
      link: "month/<Year-Month-Directory>/rr-funnel/integrations/integrations",
    },
    {
      name: "Not integrated",
      value: <GP2GP Success not Integrated>,
      link: "month/<Year-Month-Directory>/rr-funnel/integrations/integrations",
    },
    {
      name: "Error",
      value: <GP2GP Failure>,
      link: "month/<Year-Month-Directory>/rr-funnel/gp2gp/errors/errors",
    },
  ]
---

A chart representing the details of GP2GP registrations.

The same information is represented **[broken down into supplier pathways](/prm-funnel/month/<Year-Month-Directory>/rr-funnel/gp2gp/pathways/pathways.html)**

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS, "Unknown")
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
    | dedup key
    | stats count by category
    | eventstats sum(count) as total
    | sort -count
```
