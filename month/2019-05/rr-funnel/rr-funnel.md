---
layout: funnel
title:  "Requester View"
date: "2019-09-20 11:46:00 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": 420178, "link": "month/2019-05/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": 256290, "link": "month/2019-05/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": 186594, "link": "month/2019-05/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": 153935, "link": "month/2019-05/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - May 2019**.
This is the query that gave us the information:

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
