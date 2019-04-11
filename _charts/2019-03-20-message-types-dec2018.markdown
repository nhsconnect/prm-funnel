---
layout: chart
title:  "EHR extracts grouped by message type"
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
          { name: 'Large Messages', value: 81792, "link": "charts/2019-03-20-large-message-details-dec2018" },
          { name: 'Standard Messages', value: 72178, "link": "charts/2019-03-20-standard-message-details-dec2018"} 
  ]
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-31st December 2018:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```
