---
layout: chart
title:  "Standard message details"
date:   2019-03-20 11:53:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
total: 110844
chart_type: doughnut
colours: [
            "#FF6DA7",
            "#E8A333",
            "#4E8516",
            "#27DEE8",
            "#A35EFF",
            "#571845",
            "#900C3E",
            "#FF5733",
            "#FFC300"
          ]
labels: [
            "0 / 00: Success",
            "6: Patient not at surgery",
            "7: GP2GP messaging not enabled on this system",
            "10: Failed to successfully generate EHR extract",
            "19: Sender check indicates that requestor is not the patients current health care provider",
            "20: Spine system responded with an error",
            "23: Message not sent because sending practice is not large message compliant",
            "30: Large Message general failure",
            "99: Undocumented error code"
          ]
items: [
            109775,
            250,
            16,
            2,
            34,
            21,
            10,
            731,
            5
      ]
---
A chart representing the details of Standard messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st January 2019**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=0
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
