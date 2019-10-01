---
layout: funnel
title:  "Sender View"
date: "<Timestamp>"
datatype: Quantitative
confidence: Medium
datasource: NMS
categories: data
items: [
    { "name": "Requests Received", "value": <requests>, "link": "month/<Year-Month-Directory>/sr-funnel/success-vs-failure/success-vs-failure"},
    { "name": "Records Sent", "value": <retrieves> }
]
index: 2
---

The data was collected from **Splunk** with the following query, and the date range was **1st-<Month:LastDate> <Month> <Year>**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | eval is_request=1
  | eval is_retrieve=if(isnotnull(ExtractTime),1,0)
  | dedup ConversationID
  | stats sum(is_request) as requests, sum(is_retrieve) as retrieves
  | addtotals
```
