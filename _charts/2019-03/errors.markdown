---
layout: chart
title:  "GP2GP errors"
date:   2019-03-20 12:28:00 +0000
timeframe: March 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  options:
    legend:
      position: "bottom"
items: [ 
          { name: 'Unknown', value: 5608 },
          { name: 'Large message failure', value: 1686 },
          { name: 'Duplicate EHR extract received', value: 1683 },
          { name: 'TPP attachment limit', value: 336 },
          { name: 'Failed to successfully generate EHR extract', value: 233 },
          { name: 'Patient not at surgery', value: 199 },
          { name: 'A-B-A EHR extract received and rejected', value: 114 },
          { name: 'Spine system responded with an error', value: 96 },
          { name: 'Non A-B-A EHR extract received and rejected', value: 81 },
          { name: 'Failed to successfully integrate EHR extract', value: 73 },
          { name: 'EHR extract message not well formed or not able to be processed', value: 56 },
          { name: 'GP2GP not enabled on this sytem', value: 38 },
          { name: 'Non A-B-A EHR extract received and filed as an attachment', value: 10 },
          { name: 'Requester is not the patients current healthcare provider', value: 9 },
          { name: 'EHR extract received without corresponding request', value: 1 }
    ]
---
A chart representing the details of GP2GP failures.

**[Click here to see the same information broken down into supplier pathways](/prm-funnel/charts/2019-03/errors-pathways.html)**

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

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
