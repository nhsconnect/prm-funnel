---
layout: chart
title:  "EHR Extracts"
date:   2019-03-20 12:28:00 +0000
funnel_slice: EHR Extracts
timeframe: Dec 2018
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
          { name: 'Large Messages', value: 81792, "link": "month/2018-12/extracts/large/large" },
          { name: 'Standard Messages', value: 72178, "link": "month/2018-12/extracts/standard/standard"} 
  ]
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-31st December 2018:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```