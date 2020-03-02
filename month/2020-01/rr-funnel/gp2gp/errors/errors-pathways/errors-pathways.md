---
layout: errors-bar
title:  "GP2GP Errors Pathways"
date: "2020-01-12 14:10:30 +0000"
timeframe: January 2020
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
 {
    "pathway": "EMIS-EMIS",
    "unknown_count": 624,
    "lm_failure_count": 96,
    "tpp_limits_count": 1,
    "duplicate_count": 1115,
    "failed_to_generate_count": 75,
    "unknown_patient_count": 113,
    "received_and_rejected_count": 127,
    "other_count": 196,
    "Total": 2347
  },
  {
    "pathway": "EMIS-Microtest",
    "unknown_count": 20,
    "lm_failure_count": 168,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 98,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 0,
    "other_count": 11,
    "Total": 297
  },
  {
    "pathway": "EMIS-TPP",
    "unknown_count": 133,
    "lm_failure_count": 965,
    "tpp_limits_count": 0,
    "duplicate_count": 36,
    "failed_to_generate_count": 2,
    "unknown_patient_count": 31,
    "received_and_rejected_count": 29,
    "other_count": 84,
    "Total": 1280
  },
  {
    "pathway": "EMIS-Unknown",
    "unknown_count": 0,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 21,
    "other_count": 3,
    "Total": 24
  },
  {
    "pathway": "EMIS-Vision",
    "unknown_count": 1944,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 6,
    "received_and_rejected_count": 4,
    "other_count": 50,
    "Total": 2004
  },
  {
    "pathway": "TPP-EMIS",
    "unknown_count": 142,
    "lm_failure_count": 16,
    "tpp_limits_count": 301,
    "duplicate_count": 482,
    "failed_to_generate_count": 25,
    "unknown_patient_count": 20,
    "received_and_rejected_count": 70,
    "other_count": 74,
    "Total": 1130
  },
  {
    "pathway": "TPP-Microtest",
    "unknown_count": 32,
    "lm_failure_count": 129,
    "tpp_limits_count": 0,
    "duplicate_count": 2,
    "failed_to_generate_count": 105,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 0,
    "other_count": 7,
    "Total": 275
  },
  {
    "pathway": "TPP-TPP",
    "unknown_count": 10,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 3,
    "received_and_rejected_count": 0,
    "other_count": 3,
    "Total": 16
  },
  {
    "pathway": "TPP-Vision",
    "unknown_count": 447,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 4,
    "other_count": 2,
    "Total": 453
  },
]
---

A chart representing the details of GP2GP failures by supplier pathways.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2020**:

```sql
    index="gp2gp-mi" sourcetype="gppractice-RR"
        | eval key=RegistrationTime + "-" + RequestorODS + "-" + coalesce(SenderODS, "Unknown")
        | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
        | rex field=RequestorSoftware "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
        | eval RequestorSupplier=coalesce(RequestorSupplier, "Unknown")
        | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
        | rename RequestorODS as SenderODS
        | rename RequestorSoftware as SenderSoftware]
        | rex field=SenderSoftware "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
        | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName
        | eval SenderSupplier=coalesce(SenderSupplier, MName, "Unknown")
        | eval SenderSupplier=case(
            SenderSupplier=="EMIS", "EMIS",
            SenderSupplier=="TPP", "TPP",
            SenderSupplier=="INPS", "Vision",
            SenderSupplier=="Microtest", "Microtest",
            1=1, "Unknown")
        | eval RegistrationType=coalesce(RegistrationType,0)
        | eval RequestFailureType=coalesce(RequestFailureType,-1)
        | eval RequestFailurePoint=coalesce(RequestFailurePoint,-1)
        | eval RequestErrorCode=tonumber(coalesce(RequestErrorCode,-1))
        | eval ExtractAckCode=tonumber(coalesce(ExtractAckCode,-1))
        | eval ExtractEventTime=coalesce(ExtractAckTime,ExtractTime)
        | eval ExtractResult=if(ExtractAckCode==-1 and isnotnull(ExtractEventTime),0,ExtractAckCode)
        | where (RequestFailurePoint==0 and isnull(RequestFailureTime)) or
            (RegistrationType!=3 and RequestFailureType!=2 and
            RequestFailureType!=5 and RequestFailurePoint==60)
        | eval is_error=if(ExtractResult==0 or ExtractResult==15,0,1)
        | search is_error=1
        | eval service="gp2gp"
        | eval ErrorCode=if(RequestErrorCode!=-1,RequestErrorCode,ExtractResult)
        | eval pathway=RequestorSupplier + "-" + SenderSupplier
        | eval category=case(
            ErrorCode==-1,"Unknown",
            ErrorCode==23 or ErrorCode==25 or (ErrorCode >= 29 and ErrorCode <= 31),"Large message failure",
            ErrorCode==100 or ErrorCode==101,"TPP LM limits",
            ErrorCode==12,"Duplicate",
            ErrorCode==10,"Failed to generate",
            ErrorCode==6,"Unknown Patient",
            ErrorCode==17 or ErrorCode==28,"Received and rejected",
            1=1,"Other")
        | eval is_unknown=if(category=="Unknown",1,0)
        | eval is_lm_failure=if(category=="Large message failure",1,0)
        | eval is_tpp_limits=if(category=="TPP LM limits",1,0)
        | eval is_duplicate=if(category=="Duplicate",1,0)
        | eval is_failed_to_generate=if(category=="Failed to generate",1,0)
        | eval is_unknown_patient=if(category=="Unknown Patient",1,0)
        | eval is_received_and_rejected=if(category=="Received and rejected",1,0)
        | eval is_other=if(category=="Other",1,0)
        | dedup key
        | stats sum(is_unknown) as unknown_count
                sum(is_lm_failure) as lm_failure_count
                sum(is_tpp_limits) as tpp_limits_count
                sum(is_duplicate) as duplicate_count
                sum(is_failed_to_generate) as failed_to_generate_count
                sum(is_unknown_patient) as unknown_patient_count
                sum(is_received_and_rejected) as received_and_rejected_count
                sum(is_other) as other_count
                by pathway
        | addcoltotals
        | addtotals
```
