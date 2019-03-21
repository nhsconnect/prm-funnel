---
layout: chart
title:  "EHR extracts grouped by message type"
date:   2019-03-20 11:33:00 +0000
funnel_slice: EHR Extracts
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
chart_type: doughnut
colours: [
            "red",
            "blue"
          ]
labels: [
            "Large Messages",
            "Standard Messages"
          ]
items: [
            98593,
            87371
      ]
donuts: [
  { "document_name": "2019-03-20-large-message-details-feb2019" },
  { "document_name": "2019-03-20-standard-message-details-feb2019" }
] 
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-28th February 2019:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```
