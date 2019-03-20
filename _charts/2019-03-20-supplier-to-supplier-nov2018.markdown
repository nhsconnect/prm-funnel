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
total: 212153
chart_type: horizontalBar
colours: [
            "red",
            "blue",
            "pink",
            "purple",
            "yellow",
            "orange",
            "violet",
            "green",
            "grey"
          ]
labels: [
            "EMIS -> EMIS",
            "EMIS -> TPP",
            "TPP -> EMIS",
            "Vision -> EMIS",
            "Vision -> TPP",
            "MicroTest -> EMIS",
            "MicroTest -> TPP",
            "TPP -> TPP",
            "EMIS -> unknown"
          ]
items: [
            124077,
            40554,
            37431,
            6711,
            2183,
            567,
            501,
            124,
            5
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
