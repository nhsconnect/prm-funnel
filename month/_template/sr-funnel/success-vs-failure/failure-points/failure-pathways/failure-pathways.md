---
layout: extract-failure-bar
title:  "Failure Pathways"
date: "<Timestamp>"
timeframe: <Month> <Year>
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
    "pathway": "EMIS-Vision",
    "gp2_gp_disabled": <EMIS-Vision:gp2_gp_disabled>,
    "patient_not_at_surgery": <EMIS-Vision:patient_not_at_surgery>,
    "patient_lookup_failure": <EMIS-Vision:patient_lookup_failure>,
    "requestor_not_current_gp": <EMIS-Vision:requestor_not_current_gp>,
    "comms_setup": <EMIS-Vision:comms_setup>,
    "not_lm": <EMIS-Vision:not_lm>,
    "lm_problem": <EMIS-Vision:lm_problem>,
    "generate_problem": <EMIS-Vision:generate_problem>,
    "send_problem": <EMIS-Vision:send_problem>,
    "unknown": <EMIS-Vision:unknown>,
    "Total": <EMIS-Vision:Total>
  },
  {
    "pathway": "TPP-EMIS",
    "gp2_gp_disabled": <TPP-EMIS:gp2_gp_disabled>,
    "patient_not_at_surgery": <TPP-EMIS:patient_not_at_surgery>,
    "patient_lookup_failure": <TPP-EMIS:patient_lookup_failure>,
    "requestor_not_current_gp": <TPP-EMIS:requestor_not_current_gp>,
    "comms_setup": <TPP-EMIS:comms_setup>,
    "not_lm": <TPP-EMIS:not_lm>,
    "lm_problem": <TPP-EMIS:lm_problem>,
    "generate_problem": <TPP-EMIS:generate_problem>,
    "send_problem": <TPP-EMIS:send_problem>,
    "unknown": <TPP-EMIS:unknown>,
    "Total": <TPP-EMIS:Total>
  },
  {
    "pathway": "TPP-Vision",
    "gp2_gp_disabled": <TPP-Vision:gp2_gp_disabled>,
    "patient_not_at_surgery": <TPP-Vision:patient_not_at_surgery>,
    "patient_lookup_failure": <TPP-Vision:patient_lookup_failure>,
    "requestor_not_current_gp": <TPP-Vision:requestor_not_current_gp>,
    "comms_setup": <TPP-Vision:comms_setup>,
    "not_lm": <TPP-Vision:not_lm>,
    "lm_problem": <TPP-Vision:lm_problem>,
    "generate_problem": <TPP-Vision:generate_problem>,
    "send_problem": <TPP-Vision:send_problem>,
    "unknown": <TPP-Vision:unknown>,
    "Total": <TPP-Vision:Total>
  },
  {
    "pathway": "EMIS-EMIS",
    "gp2_gp_disabled": <EMIS-EMIS:gp2_gp_disabled>,
    "patient_not_at_surgery": <EMIS-EMIS:patient_not_at_surgery>,
    "patient_lookup_failure": <EMIS-EMIS:patient_lookup_failure>,
    "requestor_not_current_gp": <EMIS-EMIS:requestor_not_current_gp>,
    "comms_setup": <EMIS-EMIS:comms_setup>,
    "not_lm": <EMIS-EMIS:not_lm>,
    "lm_problem": <EMIS-EMIS:lm_problem>,
    "generate_problem": <EMIS-EMIS:generate_problem>,
    "send_problem": <EMIS-EMIS:send_problem>,
    "unknown": <EMIS-EMIS:unknown>,
    "Total": <EMIS-EMIS:Total>
  },
  {
    "pathway": "TPP-Microtest",
    "gp2_gp_disabled": <TPP-Microtest:gp2_gp_disabled>,
    "patient_not_at_surgery": <TPP-Microtest:patient_not_at_surgery>,
    "patient_lookup_failure": <TPP-Microtest:patient_lookup_failure>,
    "requestor_not_current_gp": <TPP-Microtest:requestor_not_current_gp>,
    "comms_setup": <TPP-Microtest:comms_setup>,
    "not_lm": <TPP-Microtest:not_lm>,
    "lm_problem": <TPP-Microtest:lm_problem>,
    "generate_problem": <TPP-Microtest:generate_problem>,
    "send_problem": <TPP-Microtest:send_problem>,
    "unknown": <TPP-Microtest:unknown>,
    "Total": <TPP-Microtest:Total>
  },
  {
    "pathway": "EMIS-TPP",
    "gp2_gp_disabled": <EMIS-TPP:gp2_gp_disabled>,
    "patient_not_at_surgery": <EMIS-TPP:patient_not_at_surgery>,
    "patient_lookup_failure": <EMIS-TPP:patient_lookup_failure>,
    "requestor_not_current_gp": <EMIS-TPP:requestor_not_current_gp>,
    "comms_setup": <EMIS-TPP:comms_setup>,
    "not_lm": <EMIS-TPP:not_lm>,
    "lm_problem": <EMIS-TPP:lm_problem>,
    "generate_problem": <EMIS-TPP:generate_problem>,
    "send_problem": <EMIS-TPP:send_problem>,
    "unknown": <EMIS-TPP:unknown>,
    "Total": <EMIS-TPP:Total>
  },
  {
    "pathway": "EMIS-Microtest",
    "gp2_gp_disabled": <EMIS-Microtest:gp2_gp_disabled>,
    "patient_not_at_surgery": <EMIS-Microtest:patient_not_at_surgery>,
    "patient_lookup_failure": <EMIS-Microtest:patient_lookup_failure>,
    "requestor_not_current_gp": <EMIS-Microtest:requestor_not_current_gp>,
    "comms_setup": <EMIS-Microtest:comms_setup>,
    "not_lm": <EMIS-Microtest:not_lm>,
    "lm_problem": <EMIS-Microtest:lm_problem>,
    "generate_problem": <EMIS-Microtest:generate_problem>,
    "send_problem": <EMIS-Microtest:send_problem>,
    "unknown": <EMIS-Microtest:unknown>,
    "Total": <EMIS-Microtest:Total>
  }
]
---

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

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
