---
layout: chart
title:  "Large Message Error"
date: "2019-03-22 10:32:00 +0000"
funnel_slice: EHR Extracts Sent
timeframe: Sep 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [ { name: "TPP -> EMIS", value: 170 },
  { name: "TPP -> Unknown", value: 8 },
  { name: "EMIS -> EMIS", value: 1 }]
---

A chart representing large message generic error 30 in standard messages, grouped by sending and receiving system type.

The data was collected from **Splunk** with the following queries, and the date range was the whole of September 2018:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=0 RequestAckCode=30
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
