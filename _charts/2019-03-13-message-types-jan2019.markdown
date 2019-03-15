---
layout: chart
title:  "EHR extracts grouped by message type"
date:   2019-03-05 15:46:00 +0000
funnel_slice: EHR Extracts
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
datasource: NMS
categories: data
total: 232143
chart_type: doughnut
colours: [
            "red",
            "blue"
          ]
labels: [
            "Large Messages",
            "Small Messages"
          ]
items: [
            120730,
            111413
      ]
donuts: [
  { "document_name": "2019-03-13-large-message-details-jan2019" },
  {"document_name": "2019-03-13-small-message-details-jan2019"}
] 
---
A chart representing the EHR Extracts split into message types. The data covers Emis and TPP only, as MicroTest and Vision do not report their MI.

The data was collected from **Splunk** with the following query, and the date range was 1st-31st January 2019:

```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    | join "conversationID" 
      [search index=spine2-live service="gp2gp"
        interactionID="urn:nhs:names:services:gp2gp/RCMR_IN030000UK06"
        | rename ConversationID AS conversationID]
    | dedup ConversationID
```
