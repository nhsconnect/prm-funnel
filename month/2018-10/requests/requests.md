---
layout: chart
title:  "EHR Requests"
date: "2019-03-20 12:28:00 +0000"
funnel_slice: EHR Requests Sent
timeframe: Oct 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 148053,
    "link": "month/2018-10/requests/emis-to-emis/emis-to-emis"
  },
  {
    "name": "EMIS -> TPP",
    "value": 50072,
    "link": "month/2018-10/requests/emis-to-tpp/emis-to-tpp"
  },
  {
    "name": "TPP -> EMIS",
    "value": 46953,
    "link": "month/2018-10/requests/tpp-to-emis/tpp-to-emis"
  },
  {
    "name": "Vision -> EMIS",
    "value": 7776,
    "link": "month/2018-10/requests/vision-to-emis/vision-to-emis"
  },
  {
    "name": "Vision -> TPP",
    "value": 2699,
    "link": "month/2018-10/requests/vision-to-tpp/vision-to-tpp"
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 671,
    "link": "month/2018-10/requests/microtest-to-emis/microtest-to-emis"
  },
  {
    "name": "MicroTest -> TPP",
    "value": 637,
    "link": "month/2018-10/requests/microtest-to-tpp/microtest-to-tpp"
  },
  {
    "name": "TPP -> TPP",
    "value": 129,
    "link": "month/2018-10/requests/tpp-to-tpp/tpp-to-tpp"
  },
  {
    "name": "EMIS -> unknown",
    "value": 8,
    "link": "month/2018-10/requests/emis-to-unknown/emis-to-unknown"
  },
  {
    "name": "Vision -> unknown",
    "value": 2,
    "link": "month/2018-10/requests/vision-to-unknown/vision-to-unknown" 
  }
]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-30th November 2018:

```sql
 index="gp2gp-mi" sourcetype="gppractice-RR"
    | where RequestFailurePoint=0 OR RequestFailurePoint=60 
    | join type=outer RequestorODS 
      [search index="gp2gp-mi" sourcetype="gppractice-HR"] 
    | join type=outer SenderODS 
        [search index="gp2gp-mi" sourcetype="gppractice-HR" 
          | rename RequestorODS as SenderODS 
          | rename RequestorSoftware as SenderSoftware]
    | rex field=RequestorSoftware 
      "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
    | eval RequestorSupplier=coalesce(RequestorSupplier, RequestorSupplier, "unknown")
    | rex field=SenderSoftware 
      "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
    | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName
    | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "unknown")
    | stats dc(ConversationID) as count by SenderSupplier, RequestorSupplier
    | sort - count
```
