---
layout: chart
title: "GP2GP Errors"
date: "2019-11-02 14:10:00 +0000"
timeframe: October 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data
chart_config:
  options:
    legend:
      position: "bottom"
items:
  [
    { name: "Unknown", value: 3784 },
    { name: "Duplicate EHR Extract received", value: 2366 },
    { name: "Large Message failure", value: 1386 },
    { name: "Spine system responded with an error", value: 439 },
    { name: "TPP attachment limit", value: 353 },
    { name: "Failed to successfully generate EHR Extract", value: 316 },
    { name: "Patient not at surgery", value: 293 },
    { name: "Failed to successfully integrate EHR Extract", value: 264 },
    { 
      name: "Non A-B-A EHR Extract received and rejected due to non-data related reasons", 
      value: 161 
    },
    { name: "GP2GP Messaging is not enabled on this system", value: 147 },
    { 
      name: "A-B-A EHR Extract received and rejected due to non-data related reasons", 
      value: 144 
    },
    { 
      name: "EHR Extract message not well-formed or not able to be processed", 
      value: 45 
    },
    { name: "Non A-B-A EHR Extract received and filed as attachment", value: 39 },
    { 
      name: "Sender check indicates that Requester is not the patients current healthcare provider", 
      value: 36 
    },
    { 
      name: "SDS lookup provided zero or more than one result to the query for each interaction", 
      value: 1 
    },
  ]
---

A chart representing the details of GP2GP failures.

The same information is represented **[broken down into supplier pathways](/prm-funnel/month/2019-10/rr-funnel/gp2gp/errors/errors-pathways/errors-pathways.html)**

The data was collected from **Splunk** with the following query, and the date range was **1st-31st October 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS,"Unknown")
    | eval RegistrationType=coalesce(RegistrationType,0)
    | eval RequestFailureType=coalesce(RequestFailureType,-1)
    | eval RequestFailurePoint=coalesce(RequestFailurePoint,-1)
    | eval RequestErrorCode=tonumber(coalesce(RequestErrorCode,-1))
    | eval RequestErrorLabel=if(RequestErrorCode==0,"NONE",RequestErrorCode)
    | eval ExtractAckCode=tonumber(coalesce(ExtractAckCode,-1))
    | eval ExtractEventTime=coalesce(ExtractAckTime,ExtractTime)
    | eval ExtractResult=if(ExtractAckCode==-1 and isnotnull(ExtractEventTime),0,ExtractAckCode)
    | eval ExtractResultLabel=if(ExtractResult==0,"NONE",ExtractResult)
    | where (RequestFailurePoint==0 and isnull(RequestFailureTime)) or
        (RegistrationType!=3 and RequestFailureType!=2 and
        RequestFailureType!=5 and RequestFailurePoint==60)
    | eval is_error=if(ExtractResultLabel=="NONE" or ExtractResultLabel==15,0,1)
    | search is_error=1
    | eval service="gp2gp"
    | lookup JDIE-Lookup jdiEvent AS ExtractResultLabel,service
        OUTPUTNEW JDIEText AS ExtractResultText
    | eval ExtractResultText=if (ExtractResult==100,"TPP attachment limit",ExtractResultText)
    | eval ExtractResultText=if(like(ExtractResultText,"%Large %"),
        "Large Message failure",ExtractResultText)
    | eval ExtractResultText=coalesce(ExtractResultText,"Unknown")
    | lookup JDIE-Lookup jdiEvent AS RequestErrorLabel,service
        OUTPUTNEW JDIEText AS RequestErrorText
    | eval RequestErrorText=if (RequestErrorCode==100,"TPP attachment limit",RequestErrorText)
    | eval RequestErrorText=if(like(RequestErrorText,"%Large %"),
        "Large Message failure",RequestErrorText)
    | eval RequestErrorText=coalesce(RequestErrorText,"Unknown")
    | eval JDIEText=if(RequestErrorText!="Unknown",RequestErrorText,ExtractResultText)
    | dedup key
    | stats count by JDIEText
    | eventstats sum(count) as total
    | sort -count
```
