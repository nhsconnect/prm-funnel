---
layout: chart
title:  "Large message details"
date:   2019-03-20 11:37:00 +0000
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  type: 'doughnut'
colours: [
            "#FF6DA7",
            "#E8A333",
            "#4E8516",
            "#27DEE8",
            "#A35EFF"
          ]
labels: [
            "0 / 00: Success",
            "14: Message not sent because requesting practice is not large message compliant",
            "19: Sender check indicates that requestor is not the patients current health care provider",
            "20: Spine system responded with an error",
            "23: Message not sent because sending practice is not large message compliant"
          ]
items: [
            94681,
            3235,
            15,
            131,
            529
      ]
---
A chart representing the details of Large messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-28th February 2019**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=1
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
