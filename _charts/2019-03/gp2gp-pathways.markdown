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
    "pathway": "EMIS-EMIS",
    "integrated_count": 71452,
    "not_integrated_count": 13135,
    "error_count": 1856,
    "Total": 86443
  },
  {
    "pathway": "EMIS-TPP",
    "integrated_count": 18501,
    "not_integrated_count": 4318,
    "error_count": 1123,
    "Total": 23942
  },
  {
    "pathway": "TPP-EMIS",
    "integrated_count": 8949,
    "not_integrated_count": 3234,
    "error_count": 361,
    "Total": 12544
  },
  {
    "pathway": "EMIS-Vision",
    "integrated_count": 2930,
    "not_integrated_count": 761,
    "error_count": 2600,
    "Total": 6291
  },
  {
    "pathway": "TPP-Vision",
    "integrated_count": 364,
    "not_integrated_count": 128,
    "error_count": 174,
    "Total": 666
  },
  {
    "pathway": "EMIS-Microtest",
    "integrated_count": 92,
    "not_integrated_count": 26,
    "error_count": 201,
    "Total": 319
  },
  {
    "pathway": "TPP-Microtest",
    "integrated_count": 57,
    "not_integrated_count": 40,
    "error_count": 150,
    "Total": 247
  },
  {
    "pathway": "TPP-TPP",
    "integrated_count": 0,
    "not_integrated_count": 0,
    "error_count": 6,
    "Total": 6
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
