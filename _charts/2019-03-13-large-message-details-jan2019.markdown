---
layout: chart
title:  "Large message details"
date:   2019-03-05 15:46:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
total: 120730
chart_type: doughnut
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
            115858,
            3972,
            18,
            173,
            713
      ]
---
A chart representing the details of Large messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2019**:

This is the query that gave us information on the **RequestAckCode**, specifically where this was not **0** or **00**, as we have assumed the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=1
    (RequestAckCode!=0 AND RequestAckCode!=00)
      | stats dc(ConversationID) by RequestAckCode
```
