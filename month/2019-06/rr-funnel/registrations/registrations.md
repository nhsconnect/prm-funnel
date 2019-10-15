---
layout: chart
title: "Registration details"
date: "2019-09-25 11:57:22"
timeframe: June 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Registrations
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    {
      name: "Transfer",
      value: 253350,
      "link": "month/2019-06/rr-funnel/transfers/transfers",
    },
    { name: "New registrant", value: 69823 },
    { name: "Unknown", value: 44443 },
    { name: "Patient lookup failure", value: 17455 },
    { name: "Returning registrant (no other GP)", value: 13396   },
    { name: "Already registered at practice", value: 5532 },
    { name: "GP system lookup failure", value: 8 },
  ]
---

A chart representing the breakdown of registrations by category.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th June 2019**:

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
        RegistrationType==1 and RequestFailureType==5, "New registration",
        RegistrationType==2 and RequestFailureType==5,"Returning registration (no other GP)",
        RequestFailureType==2,"Already registered",
        RequestFailurePoint==10 or RequestFailurePoint==20,"Patient lookup failure",
        RequestFailureType!=3 and RequestFailureType!=4 and
          (RequestFailurePoint==40 or RequestFailurePoint==50),"GP system lookup failure",
        (RegistrationType==3 and RequestFailureType==0) or
          RequestFailureType==3 or RequestFailureType==4 or
          (RequestFailureType !=5 and RequestFailurePoint==60) or
          (RequestFailurePoint==0 and isnull(RequestFailureTime)),"Transfer",
        1=1,"Unknown")
    | dedup key
    | stats count by category
    | eventstats sum(count) as total
    | sort -count
```
