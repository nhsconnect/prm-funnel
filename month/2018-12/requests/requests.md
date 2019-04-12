---
layout: chart
title:  "EHR Requests"
date: "2019-03-20 12:28:00 +0000"
funnel_slice: EHR Requests Sent
timeframe: Dec 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 90095,
    "link": "month/2018-12/requests/emis-to-emis/emis-to-emis"
  },
  {
    "name": "EMIS -> TPP",
    "value": 30455,
    "link": "month/2018-12/requests/emis-to-tpp/emis-to-tpp"
  },
  {
    "name": "TPP -> EMIS",
    "value": 26843,
    "link": "month/2018-12/requests/tpp-to-emis/tpp-to-emis"
  },
  {
    "name": "Vision -> EMIS",
    "value": 5448,
    "link": "month/2018-12/requests/vision-to-emis/vision-to-emis"
  },
  {
    "name": "Vision -> TPP",
    "value": 1634,
    "link": "month/2018-12/requests/vision-to-tpp/vision-to-tpp"
  },
  {
    "name": "MicroTest -> TPP",
    "value": 413,
    "link": "month/2018-12/requests/microtest-to-tpp/microtest-to-tpp"
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 387,
    "link": "month/2018-12/requests/microtest-to-emis/microtest-to-emis"
  },
  {
    "name": "TPP -> TPP",
    "value": 48,
    "link": "month/2018-12/requests/tpp-to-tpp/tpp-to-tpp"
  }
]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st December 2018:

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
