---
layout: chart
title:  "EHR extracts grouped by message type"
date:   2019-03-05 15:46:00 +0000
funnel_slice: EHR Extracts
timeframe: Jan 2019
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
          { "name": "Large Messages", "value": 120711, "link": "charts/2019-03-13-large-message-details-jan2019" },
          { "name": "Standard Messages", "value": 111376, "link": "charts/2019-03-13-standard-message-details-jan2019" }
      ]
] 
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-31st January 2019:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | stats dc(ConversationID) by LargeMessagingRequired
```
