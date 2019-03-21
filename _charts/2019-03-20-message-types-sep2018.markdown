---
layout: chart
title:  "EHR extracts grouped by message type"
date:   2019-03-20 12:28:00 +0000
funnel_slice: EHR Extracts
timeframe: Sep 2018
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  type: 'doughnut'  
  options:
    legend:
      position: "left"
colours: [
            "red",
            "blue"
          ]
labels: [
            "Large Messages",
            "Standard Messages"
          ]
items: [
            131255,
            137959
      ]
links: [
  { "document_name": "2019-03-20-large-message-details-sep2018" },
  { "document_name": "2019-03-20-standard-message-details-sep2018" }
] 
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-30th September 2018:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```
