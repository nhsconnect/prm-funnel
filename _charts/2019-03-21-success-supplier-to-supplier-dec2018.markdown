---
layout: chart
title:  "Successful integrations grouped by sending and receiving system type"
date:   2019-03-20 15:46:00 +0000
funnel_slice: Successfully Integrated
timeframe: Dec 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  type: 'horizontalBar'
colours: [
            "red",
            "blue",
            "pink",
            "purple",
            "yellow",
            "violet",
            "orange"
          ]
labels: [
            "EMIS -> EMIS",
            "TPP -> EMIS",
            "EMIS -> TPP",
            "Vision -> EMIS",
            "Vision -> TPP",
            "MicroTest -> EMIS",
            "MicroTest -> TPP"
          ]
items: [
            81517,
            22776,
            22143,
            3455,
            832,
            116,
            88
      ]
---
A chart representing the successful integrations split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was the whole of December 2018:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
    | where RequestFailurePoint=0 OR RequestFailurePoint=60 
    | where ExtractAckCode=0 OR ExtractAckCode=00
    | where ExtractAckStatus=1
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
