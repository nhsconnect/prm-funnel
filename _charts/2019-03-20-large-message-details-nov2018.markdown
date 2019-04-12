---
layout: chart
title:  "Large message details"
date: "2019-03-20 12:28:00 +0000"
timeframe: Nov 2018
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
items: [ 
          { name: '0 / 00: Success', value: 104710 },
          { name: '14: Message not sent because requesting practice is not large message compliant',
            value: 3505 },
          { name: '19: Sender check indicates that requestor is not the patients current health care provider',
            value: 18 },
          { name: '20: Spine system responded with an error', value: 134 },
          { name: '23: Message not sent because sending practice is not large message compliant',
            value: 642 },
          { name: '99: Undocumented error code', value: 1 } 
        ]
---
A chart representing the details of Large messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th November 2018**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=1
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
