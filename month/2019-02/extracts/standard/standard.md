---
layout: chart
title:  "Standard message details"
date: "2019-03-20 11:53:00 +0000"
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "0 / 00: Success",
    "value": 86027
  },
  {
    "name": "6: Patient not at surgery",
    "value": 203
  },
  {
    "name": "7: GP2GP messaging not enabled on this system",
    "value": 18
  },
  {
    "name": "10: Failed to successfully generate EHR extract",
    "value": 4
  },
  {
    "name": "19: Sender check indicates that requestor is not the patients current health care provider",
    "value": 16
  },
  {
    "name": "20: Spine system responded with an error",
    "value": 10
  },
  {
    "name": "23: Message not sent because sending practice is not large message compliant",
    "value": 12
  },
  {
    "name": "24: SDS lookup provided zero or more than one result to the query for each interaction",
    "value": 1
  },
  {
    "name": "30: Large Message general failure",
    "value": 638,
    "link": "month/2019-02/extracts/standard/large-message-error/large-message-error"
  },
  {
    "name": "99: Undocumented error code",
    "value": 5
  }
]
---
A chart representing the details of Standard messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-28th February 2019**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=0
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
