---
layout: chart
title:  "EHR Requests sent grouped by sending and receiving system type"
date:   2019-03-20 12:28:00 +0000
funnel_slice: EHR Requests Sent
timeframe: Oct 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "EMIS -> EMIS",
    "value": 148053
  },
  {
    "name": "EMIS -> TPP",
    "value": 50072
  },
  {
    "name": "TPP -> EMIS",
    "value": 46953
  },
  {
    "name": "Vision -> EMIS",
    "value": 7776
  },
  {
    "name": "Vision -> TPP",
    "value": 2699
  },
  {
    "name": "MicroTest -> EMIS",
    "value": 671
  },
  {
    "name": "MicroTest -> TPP",
    "value": 637
  },
  {
    "name": "TPP -> TPP",
    "value": 129
  },
  {
    "name": "EMIS -> unknown",
    "value": 8
  },
  {
    "name": "Vision -> unknown",
    "value": 2
  }
]
links: [
  { "document_name": "charts/extract-ack-codes/oct2018/emis-to-emis-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/emis-to-tpp-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/tpp-to-emis-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/vision-to-emis-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/vision-to-tpp-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/microtest-to-emis-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/microtest-to-tpp-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/tpp-to-tpp-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/emis-to-unknown-extract-ack-codes" },
  { "document_name": "charts/extract-ack-codes/oct2018/vision-to-unknown-extract-ack-codes" }
]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st October 2018:

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
