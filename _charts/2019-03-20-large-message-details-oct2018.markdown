---
layout: chart
title:  "Large message details"
date:   2019-03-20 12:28:00 +0000
timeframe: Oct 2018
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
            "23: Message not sent because sending practice is not large message compliant",
            "99: Undocumented error code"
          ]
items: [
            123219,
            4100,
            24,
            172,
            736,
            1
      ]
---
A chart representing the details of Large messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st October 2018**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=1
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
