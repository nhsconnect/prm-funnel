---
layout: extract-failure-bar
title:  "Failure Pathways"
date: "2019-10-02 09:24:15"
timeframe: August 2019
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
    "gp2_gp_disabled": 35,
    "patient_not_at_surgery": 84,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 13,
    "comms_setup": 0,
    "not_lm": 8,
    "lm_problem": 5,
    "generate_problem": 5,
    "send_problem": 81,
    "unknown": 340,
    "Total": 571
  },
  {
    "pathway": "EMIS-Microtest",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 187,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 2,
    "Total": 189
  },
  {
    "pathway": "EMIS-TPP",
    "gp2_gp_disabled": 9,
    "patient_not_at_surgery": 36,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 4,
    "comms_setup": 0,
    "not_lm": 0,
    "lm_problem": 0,
    "generate_problem": 1,
    "send_problem": 53,
    "unknown": 105,
    "Total": 208
  },
  {
    "pathway": "EMIS-Unknown",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 1,
    "comms_setup": 0,
    "not_lm": 0,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 4,
    "Total": 5
  },
  {
    "pathway": "EMIS-Vision",
    "gp2_gp_disabled": 3,
    "patient_not_at_surgery": 1,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 4,
    "comms_setup": 0,
    "not_lm": 1751,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 22,
    "Total": 1781
  },
  {
    "pathway": "TPP-EMIS",
    "gp2_gp_disabled": 1,
    "patient_not_at_surgery": 24,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 2,
    "comms_setup": 1,
    "not_lm": 3,
    "lm_problem": 777,
    "generate_problem": 0,
    "send_problem": 39,
    "unknown": 47,
    "Total": 894
  },
  {
    "pathway": "TPP-Microtest",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 288,
    "lm_problem": 10,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 0,
    "Total": 298
  },
  {
    "pathway": "TPP-TPP",
    "gp2_gp_disabled": 2,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 0,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 0,
    "Total": 2
  },
  {
    "pathway": "TPP-Vision",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 978,
    "lm_problem": 17,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 1,
    "Total": 996
  },
  {
    "pathway": "Unknown-EMIS",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 0,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 0,
    "Total": 0
  },
  {
    "pathway": "Unknown-Vision",
    "gp2_gp_disabled": 0,
    "patient_not_at_surgery": 0,
    "patient_lookup_failure": 0,
    "requestor_not_current_gp": 0,
    "comms_setup": 0,
    "not_lm": 3,
    "lm_problem": 0,
    "generate_problem": 0,
    "send_problem": 0,
    "unknown": 0,
    "Total": 3
  },
]
---

The data was collected from **Splunk** with the following query, and the date range was **1st-31st August 2019**:

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
