---
layout: chart
title: "Transfers"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: Transfers
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    {
      name: "GP2GP",
      value: <GP2GP>,
      "link": "month/<Year-Month-Directory>/rr-funnel/gp2gp/gp2gp",
    },
    { name: "TPP internal", value: <Internal Transfer> },
    { name: "Non GP2GP practice", value: <Transfer from non-GP2GP practice> },
  ]
---

A chart representing the details of transfer registrations.

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
        RequestFailureType==3 or RequestFailureType==4,"Transfer from non-GP2GP practice",
        RegistrationType==3 and RequestFailureType==0,"Internal Transfer",
        (RequestFailurePoint==0 and isnull(RequestFailureTime)) or
          (RegistrationType!=3 and RequestFailureType!=2 and
          RequestFailureType!=5 and RequestFailurePoint==60),"GP2GP")
    | dedup key
    | stats count by category
    | eventstats sum(count) as total
    | sort -count
```
