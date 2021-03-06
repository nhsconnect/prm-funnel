---
layout: chart
title:  "EHR extracts"
date: "2019-03-20 11:33:00 +0000"
funnel_slice: EHR Extracts
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data  
chart_config: 
  type: 'doughnut'
  options:
    legend:
      position: "left"
items: [
  {
    "name": "Large Messages",
    "value": 98593,
    "link": "month/2019-02/extracts/large/large"
  },
  {
    "name": "Standard Messages",
    "value": 87371,
    "link": "month/2019-02/extracts/standard/standard"
  }
]
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-28th February 2019:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```
