---
layout: extract-failure-bar
title:  "Failure Pathways"
date: "2019-09-25 09:24:15"
timeframe: June 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests received
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  options:
    legend:
      position: "bottom"
items: [ 
    {
      "pathway": "EMIS-EMIS",
      "gp2_gp_disabled": 38,
      "patient_not_at_surgery": 243,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 19,
      "comms_setup": 0,
      "not_lm": 25,
      "lm_problem": 3,
      "generate_problem": 1,
      "send_problem": 53,
      "unknown": 314,
      "Total": 696
    },
    {
      "pathway": "EMIS-Microtest",
      "gp2_gp_disabled": 0,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 0,
      "comms_setup": 0,
      "not_lm": 154,
      "lm_problem": 0,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 1,
      "Total": 155
    },
    {
      "pathway": "EMIS-TPP",
      "gp2_gp_disabled": 13,
      "patient_not_at_surgery": 27,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 6,
      "comms_setup": 0,
      "not_lm": 1,
      "lm_problem": 0,
      "generate_problem": 2,
      "send_problem": 53,
      "unknown": 114,
      "Total": 216
    },
    {
      "pathway": "EMIS-Unknown",
      "gp2_gp_disabled": 5,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 10,
      "comms_setup": 0,
      "not_lm": 0,
      "lm_problem": 0,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 5,
      "Total": 20   
    },
    {
      "pathway": "EMIS-Vision",
      "gp2_gp_disabled": 6,
      "patient_not_at_surgery": 2,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 5,
      "comms_setup": 0,
      "not_lm": 1722,
      "lm_problem": 0,
      "generate_problem": 0,
      "send_problem": 2,
      "unknown": 30,
      "Total": 1767
    },
    {
      "pathway": "TPP-EMIS",
      "gp2_gp_disabled": 20,
      "patient_not_at_surgery": 39,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 1,
      "comms_setup": 0,
      "not_lm": 20,
      "lm_problem": 639,
      "generate_problem": 0,
      "send_problem": 28,
      "unknown": 36,
      "Total": 783
    },
    {
      "pathway": "TPP-Microtest",
      "gp2_gp_disabled": 0,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 1,
      "comms_setup": 0,
      "not_lm": 281,
      "lm_problem": 17,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 1,
      "Total": 300
    },
    {
      "pathway": "TPP-TPP",
      "gp2_gp_disabled": 6,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 0,
      "comms_setup": 0,
      "not_lm": 0,
      "lm_problem": 1,
      "generate_problem": 0,
      "send_problem": 1,
      "unknown": 0,
      "Total": 8
    },
    {
      "pathway": "TPP-Vision",
      "gp2_gp_disabled": 0,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 0,
      "comms_setup": 0,
      "not_lm": 880,
      "lm_problem": 15,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 2,
      "Total": 897
    },
    {
      "pathway": "Unknown-EMIS",
      "gp2_gp_disabled": 0,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 0,
      "comms_setup": 0,
      "not_lm": 0,
      "lm_problem": 1,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 0,
      "Total": 1
    },
    {
      "pathway": "Unknown-Vision",
      "gp2_gp_disabled": 0,
      "patient_not_at_surgery": 0,
      "patient_lookup_failure": 0,
      "requestor_not_current_gp": 0,
      "comms_setup": 0,
      "not_lm": 1,
      "lm_problem": 0,
      "generate_problem": 0,
      "send_problem": 0,
      "unknown": 0,
      "Total": 1
    },
]
---

The data was collected from **Splunk** with the following query, and the date range was **1st-30th June 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | join type=outer SenderODS [search index="gp2gp-mi" sourcetype="gppractice-HR"
      | rename RequestorODS as SenderODS
      | rename RequestorSoftware as SenderSoftware]
  | rex field=SenderSoftware "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
  | eval SenderSupplier=coalesce(SenderSupplier, "Unknown")
  | join type=outer RequestorODS [search index="gp2gp-mi" sourcetype="gppractice-HR"]
  | rex field=RequestorSoftware "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
  | lookup Spine2-NACS-Lookup NACS AS RequestorODS OUTPUTNEW MName AS MName
  | eval RequestorSupplier=coalesce(RequestorSupplier, MName, "Unknown")
  | eval RequestorSupplier=case(
      RequestorSupplier=="EMIS", "EMIS",
      RequestorSupplier=="TPP", "TPP",
      RequestorSupplier=="INPS", "Vision",
      RequestorSupplier=="Microtest", "Microtest",
      1=1, "Unknown")
  | eval ExtractFailurePoint=coalesce(ExtractFailurePoint, -1)
  | eval RequestAckCode=coalesce(RequestAckCode, -1)
  | eval RequestAckCode=tonumber(RequestAckCode)
  | eval category=case(
      ExtractFailurePoint==0 and RequestAckCode==0,"Success",
      ExtractFailurePoint==0 and RequestAckCode==7,"GP2GP disabled",
      ExtractFailurePoint==10 and RequestAckCode==6,"Patient not at surgery",
      ExtractFailurePoint==10, "Patient lookup failure",
      ExtractFailurePoint==20,"Requestor not current GP",
      ExtractFailurePoint==30 or ExtractFailurePoint==40,"Communications setup failure",
      ExtractFailurePoint==50 and RequestAckCode==14,"Requester not large message compliant",
      ExtractFailurePoint==50,"Large message failure",
      ExtractFailurePoint==60 and RequestAckCode==10,"Unable to generate EHR extract",
      ExtractFailurePoint==60 and RequestAckCode==30,"Large message failure",
      ExtractFailurePoint==60,"Unable to send EHR extract",
      1=1,"Unknown issue")
  | eval pathway = SenderSupplier + "-" + RequestorSupplier
  | eval is_gp2_gp_disabled=if(category=="GP2GP disabled",1,0)
  | eval is_patient_not_at_surgery=if(category=="Patient not at surgery",1,0)
  | eval is_patient_lookup_failure=if(category=="Patient lookup failure",1,0)
  | eval is_requestor_not_current_gp=if(category=="Requestor not current GP",1,0)
  | eval is_comms_setup=if(category=="Communications setup failure",1,0)
  | eval is_not_lm=if(category=="Requester not large message compliant",1,0)
  | eval is_lm_problem=if(category=="Large message failure",1,0)
  | eval is_generate_problem=if(category=="Unable to generate EHR extract",1,0)
  | eval is_send_problem=if(category=="Unable to send EHR extract",1,0)
  | eval is_unknown=if(category=="Unknown issue",1,0)
  | dedup ConversationID
  | stats sum(is_gp2_gp_disabled) as gp2_gp_disabled,
          sum(is_patient_not_at_surgery) as patient_not_at_surgery,
          sum(is_patient_lookup_failure) as patient_lookup_failure,
          sum(is_requestor_not_current_gp) as requestor_not_current_gp,
          sum(is_comms_setup) as comms_setup,
          sum(is_not_lm) as not_lm,
          sum(is_lm_problem) as lm_problem,
          sum(is_generate_problem) as generate_problem,
          sum(is_send_problem) as send_problem,
          sum(is_unknown) as unknown
    by pathway
  | addcoltotals
  | addtotals
```
