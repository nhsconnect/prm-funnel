---
layout: chart
title:  "Standard message details"
date:   2019-03-20 12:28:00 +0000
timeframe: Sep 2018
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Extracts
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "0 / 00: Success",
    "value": 136177
  },
  {
    "name": "6: Patient not at surgery",
    "value": 261
  },
  {
    "name": "7: GP2GP messaging not enabled on this system",
    "value": 92
  },
  {
    "name": "10: Failed to successfully generate EHR extract",
    "value": 9
  },
  {
    "name": "19: Sender check indicates that requestor is not the patients current health care provider",
    "value": 29
  },
  {
    "name": "20: Spine system responded with an error",
    "value": 141
  },
  {
    "name": "23: Message not sent because sending practice is not large message compliant",
    "value": 22
  },
  {
    "name": "30: Large Message general failure",
    "value": 656
  },
  {
    "name": "99: Undocumented error code",
    "value": 4
  }
]
links: [
  {},
  {},
  {},
  {},
  {},
  {},
  {},
  { "document_name": "charts/2019-03-22-large-msg-30-supplier-to-supplier-sep2018" },
  {}
]
---
A chart representing the details of Standard messages.

The data was collected from **Splunk** with the following query, and the date range was **1st-30th September 2018**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
 index="gp2gp-mi" sourcetype="gppractice-SR"
    LargeMessagingRequired=0
      | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
      | stats dc(ConversationID) by RequestAckCode
```
