---
layout: chart
title:  "EHR Requests sent grouped by sending and receiving system type"
date:   2019-03-20 12:28:00 +0000
funnel_slice: EHR Requests Sent
timeframe: Nov 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 124077,
    "link": "charts/extract-ack-codes/nov2018/emis-to-emis-extract-ack-codes"
  },
  {
    "name": "EMIS -> TPP",
    "value": 40554,
    "link": "charts/extract-ack-codes/nov2018/emis-to-tpp-extract-ack-codes"
  },
  {
    "name": "TPP -> EMIS",
    "value": 37431,
    "link": "charts/extract-ack-codes/nov2018/tpp-to-emis-extract-ack-codes"
  },
  {
    "name": "Vision -> EMIS",
    "value": 6711,
    "link": "charts/extract-ack-codes/nov2018/vision-to-emis-extract-ack-codes"
  },
  {
    "name": "Vision -> TPP",
    "value": 2183,
    "link": "charts/extract-ack-codes/nov2018/vision-to-tpp-extract-ack-codes"
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 567,
    "link": "charts/extract-ack-codes/nov2018/microtest-to-emis-extract-ack-codes"
  },
  {
    "name": "MicroTest -> TPP",
    "value": 501,
    "link": "charts/extract-ack-codes/nov2018/microtest-to-tpp-extract-ack-codes"
  },
  {
    "name": "TPP -> TPP",
    "value": 124,
    "link": "charts/extract-ack-codes/nov2018/tpp-to-tpp-extract-ack-codes"
  },
  {
    "name": "EMIS -> unknown",
    "value": 5,
    "link": "charts/extract-ack-codes/nov2018/emis-to-unknown-extract-ack-codes"
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
