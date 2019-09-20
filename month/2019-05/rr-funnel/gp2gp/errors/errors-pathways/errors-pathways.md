---
layout: errors-bar
title:  "GP2GP Errors Pathways"
date: "2019-09-20 12:28:00 +0000"
timeframe: May 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-Vision",
    "unknown_count": 1456,
    "lm_failure_count": 1,
    "tpp_limits_count": 0,
    "duplicate_count": 14,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 7,
    "received_and_rejected_count": 0,
    "other_count": 101,
    "Total": 1579
  },
  {
    "pathway": "EMIS-EMIS",
    "unknown_count": 1417,
    "lm_failure_count": 17,
    "tpp_limits_count": 2,
    "duplicate_count": 845,
    "failed_to_generate_count": 6,
    "unknown_patient_count": 110,
    "received_and_rejected_count": 76,
    "other_count": 718,
    "Total": 3191
  },
  {
    "pathway": "EMIS-TPP",
    "unknown_count": 224,
    "lm_failure_count": 1107,
    "tpp_limits_count": 0,
    "duplicate_count": 27,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 21,
    "received_and_rejected_count": 36,
    "other_count": 257,
    "Total": 1672
  },
  {
    "pathway": "TPP-EMIS",
    "unknown_count": 379,
    "lm_failure_count": 15,
    "tpp_limits_count": 343,
    "duplicate_count": 403,
    "failed_to_generate_count": 5,
    "unknown_patient_count": 38,
    "received_and_rejected_count": 47,
    "other_count": 107,
    "Total": 1337
  },
  {
    "pathway": "TPP-Vision",
    "unknown_count": 470,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 6,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 2,
    "other_count": 1,
    "Total": 479
  },
  {
    "pathway": "TPP-Microtest",
    "unknown_count": 20,
    "lm_failure_count": 156,
    "tpp_limits_count": 0,
    "duplicate_count": 1,
    "failed_to_generate_count": 126,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 1,
    "other_count": 14,
    "Total": 318
  },
  {
    "pathway": "EMIS-Microtest",
    "unknown_count": 5,
    "lm_failure_count": 121,
    "tpp_limits_count": 0,
    "duplicate_count": 5,
    "failed_to_generate_count": 73,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 19,
    "other_count": 19,
    "Total": 223
  },
  { 
    "pathway": "TPP-TPP",
    "unknown_count": 23,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 6,
    "received_and_rejected_count": 0,
    "other_count": 36,
    "Total": 65
  },
  { 
    "pathway": "Vision-EMIS",
    "unknown_count": 111,
    "lm_failure_count": 1,
    "tpp_limits_count": 0,
    "duplicate_count": 72,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 10,
    "received_and_rejected_count": 15,
    "other_count": 117,
    "Total": 326
  },
  { 
    "pathway": "Vision-Microtest",
    "unknown_count": 3,
    "lm_failure_count": 24,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 12,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 0,
    "other_count": 2,
    "Total": 41
  }
]
---

A chart representing the details of GP2GP failures by supplier pathways.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st May 2019**:

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
            SenderSupplier=="Vision", "Vision",
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
