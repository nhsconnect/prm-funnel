---
layout: chart
title: "Integration Details"
date: "2020-01-12 14:10:30 +0000"
timeframe: January 2020
datatype: Quantitative
confidence: Medium
funnel_slice: Integrations
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    { name: "Integrated", value: 171990 },
    { name: "Not acknowledged", value: 29916 },
    { name: "Not sent", value: 11389 },
    { name: "Suppressed", value: 10351 },
    { name: "Duplicate", value: 953 },
    { name: "Other", value: 302 },
    { name: "Filing rejected", value: 278 },
    { name: "Filing failed", value: 100 },
    { name: "Large message failure", value: 99 },
    { name: "Filed as attachment", value: 4 },
    { name: "Not requested", value: 2 },
  ]
---

A chart representing the details of GP2GP integrations.

The same information about the filing of records is represented **[broken down into supplier pathways](/prm-funnel/month/2020-01/rr-funnel/integrations/filing-by-requestor/filing-by-requestor.html)**

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2020**:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS,"Unknown")
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
        ExtractAckStatus==4,"Not requested",
        ExtractAckStatus==5 and ExtractResultLabel==15,"Suppressed",
        ExtractAckStatus==5 and ExtractResultLabel!=15,"Filed as attachment",
        ExtractAckStatus==6,"Large message failure",
        ExtractAckStatus==7,"Filing failed",
        1=1,"Other")
    | where (RequestFailurePoint==0 and isnull(RequestFailureTime))
        or (RegistrationType!=3 and RequestFailureType!=2 and
        RequestFailureType!=5 and RequestFailurePoint==60)
    | dedup key
    | stats count by ExtractAckStatusLabel
    | eventstats sum(count) as total
    | sort -count
```
