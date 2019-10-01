---
layout: errors-bar
title:  "GP2GP Errors Pathways"
date: "<Timestamp>"
timeframe: <Month> <Year>
datatype: Quantitative
confidence: Medium
funnel_slice: GP2GP
datasource: NMS (gp2gp-mi)
categories: data    
items: [
  {
    "pathway": "EMIS-Vision",
    "unknown_count": <EMIS-Vision:unknown_count>,
    "lm_failure_count": <EMIS-Vision:lm_failure_count>,
    "tpp_limits_count": <EMIS-Vision:tpp_limits_count>,
    "duplicate_count": <EMIS-Vision:duplicate_count>,
    "failed_to_generate_count": <EMIS-Vision:failed_to_generate_count>,
    "unknown_patient_count": <EMIS-Vision:unknown_patient_count>,
    "received_and_rejected_count": <EMIS-Vision:received_and_rejected_count>,
    "other_count": <EMIS-Vision:other_count>,
    "Total": <EMIS-Vision:Total>
  },
  {
    "pathway": "EMIS-EMIS",
    "unknown_count": <EMIS-EMIS:unknown_count>,
    "lm_failure_count": <EMIS-EMIS:lm_failure_count>,
    "tpp_limits_count": <EMIS-EMIS:tpp_limits_count>,
    "duplicate_count": <EMIS-EMIS:duplicate_count>,
    "failed_to_generate_count": <EMIS-EMIS:failed_to_generate_count>,
    "unknown_patient_count": <EMIS-EMIS:unknown_patient_count>,
    "received_and_rejected_count": <EMIS-EMIS:received_and_rejected_count>,
    "other_count": <EMIS-EMIS:other_count>,
    "Total": <EMIS-EMIS:Total>
  },
  {
    "pathway": "EMIS-TPP",
    "unknown_count": <EMIS-TPP:unknown_count>,
    "lm_failure_count": <EMIS-TPP:lm_failure_count>,
    "tpp_limits_count": <EMIS-TPP:tpp_limits_count>,
    "duplicate_count": <EMIS-TPP:duplicate_count>,
    "failed_to_generate_count": <EMIS-TPP:failed_to_generate_count>,
    "unknown_patient_count": <EMIS-TPP:unknown_patient_count>,
    "received_and_rejected_count": <EMIS-TPP:received_and_rejected_count>,
    "other_count": <EMIS-TPP:other_count>,
    "Total": <EMIS-TPP:Total>
  },
  {
    "pathway": "TPP-EMIS",
    "unknown_count": <TPP-EMIS:unknown_count>,
    "lm_failure_count": <TPP-EMIS:lm_failure_count>,
    "tpp_limits_count": <TPP-EMIS:tpp_limits_count>,
    "duplicate_count": <TPP-EMIS:duplicate_count>,
    "failed_to_generate_count": <TPP-EMIS:failed_to_generate_count>,
    "unknown_patient_count": <TPP-EMIS:unknown_patient_count>,
    "received_and_rejected_count": <TPP-EMIS:received_and_rejected_count>,
    "other_count": <TPP-EMIS:other_count>,
    "Total": <TPP-EMIS:Total>
  },
  {
    "pathway": "TPP-Vision",
    "unknown_count": <TPP-Vision:unknown_count>,
    "lm_failure_count": <TPP-Vision:lm_failure_count>,
    "tpp_limits_count": <TPP-Vision:tpp_limits_count>,
    "duplicate_count": <TPP-Vision:duplicate_count>,
    "failed_to_generate_count": <TPP-Vision:failed_to_generate_count>,
    "unknown_patient_count": <TPP-Vision:unknown_patient_count>,
    "received_and_rejected_count": <TPP-Vision:received_and_rejected_count>,
    "other_count": <TPP-Vision:other_count>,
    "Total": <TPP-Vision:Total>
  },
  {
    "pathway": "TPP-Microtest",
    "unknown_count": <TPP-Microtest:unknown_count>,
    "lm_failure_count": <TPP-Microtest:lm_failure_count>,
    "tpp_limits_count": <TPP-Microtest:tpp_limits_count>,
    "duplicate_count": <TPP-Microtest:duplicate_count>,
    "failed_to_generate_count": <TPP-Microtest:failed_to_generate_count>,
    "unknown_patient_count": <TPP-Microtest:unknown_patient_count>,
    "received_and_rejected_count": <TPP-Microtest:received_and_rejected_count>,
    "other_count": <TPP-Microtest:other_count>,
    "Total": <TPP-Microtest:Total>
  },
  {
    "pathway": "EMIS-Microtest",
    "unknown_count": <EMIS-Microtest:unknown_count>,
    "lm_failure_count": <EMIS-Microtest:lm_failure_count>,
    "tpp_limits_count": <EMIS-Microtest:tpp_limits_count>,
    "duplicate_count": <EMIS-Microtest:duplicate_count>,
    "failed_to_generate_count": <EMIS-Microtest:failed_to_generate_count>,
    "unknown_patient_count": <EMIS-Microtest:unknown_patient_count>,
    "received_and_rejected_count": <EMIS-Microtest:received_and_rejected_count>,
    "other_count": <EMIS-Microtest:other_count>,
    "Total": <EMIS-Microtest:Total>
  },
  { 
    "pathway": "TPP-TPP",
    "unknown_count": <TPP-TPP:unknown_count>,
    "lm_failure_count": <TPP-TPP:lm_failure_count>,
    "tpp_limits_count": <TPP-TPP:tpp_limits_count>,
    "duplicate_count": <TPP-TPP:duplicate_count>,
    "failed_to_generate_count": <TPP-TPP:failed_to_generate_count>,
    "unknown_patient_count": <TPP-TPP:unknown_patient_count>,
    "received_and_rejected_count": <TPP-TPP:received_and_rejected_count>,
    "other_count": <TPP-TPP:other_count>,
    "Total": <TPP-TPP:Total>
  },
  { 
    "pathway": "Vision-EMIS",
    "unknown_count": <Vision-EMIS:unknown_count>,
    "lm_failure_count": <Vision-EMIS:lm_failure_count>,
    "tpp_limits_count": <Vision-EMIS:tpp_limits_count>,
    "duplicate_count": <Vision-EMIS:duplicate_count>,
    "failed_to_generate_count": <Vision-EMIS:failed_to_generate_count>,
    "unknown_patient_count": <Vision-EMIS:unknown_patient_count>,
    "received_and_rejected_count": <Vision-EMIS:received_and_rejected_count>,
    "other_count": <Vision-EMIS:other_count>,
    "Total": <Vision-EMIS:Total>
  },
  { 
    "pathway": "Vision-Microtest",
    "unknown_count": <Vision-Microtest:unknown_count>,
    "lm_failure_count": <Vision-Microtest:lm_failure_count>,
    "tpp_limits_count": <Vision-Microtest:tpp_limits_count>,
    "duplicate_count": <Vision-Microtest:duplicate_count>,
    "failed_to_generate_count": <Vision-Microtest:failed_to_generate_count>,
    "unknown_patient_count": <Vision-Microtest:unknown_patient_count>,
    "received_and_rejected_count": <Vision-Microtest:received_and_rejected_count>,
    "other_count": <Vision-Microtest:other_count>,
    "Total": <Vision-Microtest:Total>
  }
]
---

A chart representing the details of GP2GP failures by supplier pathways.

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

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
