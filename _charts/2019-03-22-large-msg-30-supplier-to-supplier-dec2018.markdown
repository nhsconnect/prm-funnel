---
layout: chart
title:  "Large message generic error 30 in standard messages, grouped by sending and receiving system type"
date:   2019-03-22 10:30:00 +0000
funnel_slice: EHR Extracts Sent
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
            "purple"
          ]
labels: [
            "TPP -> EMIS",
            "TPP -> Unknown",
            "EMIS -> EMIS",
            "EMIS -> Unknown"
          ]
items: [
            462,
            30,
            4,
            1
      ]
---
A chart representing the successful integrations split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was the whole of December 2018:

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
