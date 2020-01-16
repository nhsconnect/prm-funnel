---
layout: errors-bar
title:  "GP2GP Errors Pathways"
date: "2019-12-02 14:10:30 +0000"
timeframe: November 2019
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-EMIS",
    "unknown_count": 546,
    "lm_failure_count": 72,
    "tpp_limits_count": 2,
    "duplicate_count": 903,
    "failed_to_generate_count": 23,
    "unknown_patient_count": 184,
    "received_and_rejected_count": 130,
    "other_count": 266,
    "Total": 2126
  },
  {
    "pathway": "EMIS-Microtest",
    "unknown_count": 25,
    "lm_failure_count": 136,
    "tpp_limits_count": 0,
    "duplicate_count": 1,
    "failed_to_generate_count": 165,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 1,
    "other_count": 10,
    "Total": 338
  },
  {
    "pathway": "EMIS-TPP",
    "unknown_count": 110,
    "lm_failure_count": 775,
    "tpp_limits_count": 0,
    "duplicate_count": 38,
    "failed_to_generate_count": 5,
    "unknown_patient_count": 30,
    "received_and_rejected_count": 42,
    "other_count": 93,
    "Total": 1093
  },
  {
    "pathway": "EMIS-Unknown",
    "unknown_count": 0,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 0,
    "received_and_rejected_count": 0,
    "other_count": 1,
    "Total": 1
  },
  {
    "pathway": "EMIS-Vision",
    "unknown_count": 1745,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 2,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 1,
    "received_and_rejected_count": 3,
    "other_count": 46,
    "Total": 1797
  },
  {
    "pathway": "TPP-EMIS",
    "unknown_count": 128,
    "lm_failure_count": 17,
    "tpp_limits_count": 295,
    "duplicate_count": 457,
    "failed_to_generate_count": 11,
    "unknown_patient_count": 31,
    "received_and_rejected_count": 52,
    "other_count": 88,
    "Total": 1079
  },
  {
    "pathway": "TPP-Microtest",
    "unknown_count": 110,
    "lm_failure_count": 177,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 706,
    "unknown_patient_count": 2,
    "received_and_rejected_count": 0,
    "other_count": 16,
    "Total": 1011
  },
  {
    "pathway": "TPP-TPP",
    "unknown_count": 17,
    "lm_failure_count": 5,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 5,
    "unknown_patient_count": 16,
    "received_and_rejected_count": 0,
    "other_count": 10,
    "Total": 53
  },
  {
    "pathway": "TPP-Unknown",
    "unknown_count": 0,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 2,
    "received_and_rejected_count": 0,
    "other_count": 0,
    "Total": 2
  },
  {
    "pathway": "TPP-Vision",
    "unknown_count": 512,
    "lm_failure_count": 0,
    "tpp_limits_count": 0,
    "duplicate_count": 0,
    "failed_to_generate_count": 0,
    "unknown_patient_count": 1,
    "received_and_rejected_count": 1,
    "other_count": 0,
    "Total": 514
  },
  {
    "pathway": "Unknown",
    "unknown_count": 3193,
    "lm_failure_count": 1182,
    "tpp_limits_count": 297,
    "duplicate_count": 1401,
    "failed_to_generate_count": 915,
    "unknown_patient_count": 267,
    "received_and_rejected_count": 229,
    "other_count": 530,
    "Total": 8014
  }
]
---

A chart representing the details of GP2GP failures by supplier pathways.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th November 2019**:

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
