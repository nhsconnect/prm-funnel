---
layout: chart
title:  "EHR Requests sent grouped by sending and receiving system type"
date: "2019-03-20 11:32:00 +0000"
funnel_slice: EHR Requests Sent
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 90095,
    "link": "charts/extract-ack-codes/feb2019/emis-to-emis-extract-ack-codes"
  },
  {
    "name": "EMIS -> TPP",
    "value": 30455,
    "link": "charts/extract-ack-codes/feb2019/emis-to-tpp-extract-ack-codes"
  },
  {
    "name": "TPP -> EMIS",
    "value": 26843,
    "link": "charts/extract-ack-codes/feb2019/tpp-to-emis-extract-ack-codes"
  },
  {
    "name": "Vision -> EMIS",
    "value": 5448,
    "link": "charts/extract-ack-codes/feb2019/vision-to-emis-extract-ack-codes"
  },
  {
    "name": "Vision -> TPP",
    "value": 1634,
    "link": "charts/extract-ack-codes/feb2019/vision-to-tpp-extract-ack-codes"
  },
  {
    "name": "MicroTest -> TPP",
    "value": 413,
    "link": "charts/extract-ack-codes/feb2019/microtest-to-emis-extract-ack-codes"
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 387,
    "link": "charts/extract-ack-codes/feb2019/microtest-to-tpp-extract-ack-codes"
  },
  {
    "name": "TPP -> TPP",
    "value": 48,
    "link": "charts/extract-ack-codes/feb2019/tpp-to-tpp-extract-ack-codes"
  }
]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-28th February 2019:

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
