---
layout: chart
title:  "Large message details"
date: "2019-03-05 15:46:00 +0000"
timeframe: Jan 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
items: [ 
          { name: '0 / 00: Success', value: 115837 },
          { name: '14: Message not sent because requesting practice is not large message compliant',
            value: 3972 },
          { name: '19: Sender check indicates that requestor is not the patients current health care provider',
            value: 18 },
          { name: '20: Spine system responded with an error', value: 173 },
          { name: '23: Message not sent because sending practice is not large message compliant',
    value: 713 } 
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
