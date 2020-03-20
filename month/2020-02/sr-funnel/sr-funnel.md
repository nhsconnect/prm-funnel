---
layout: funnel
title: "Sender View"
date: "2020-02-12 14:10:00 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS
categories: data
items:
  [
    {
      "name": "Requests Received",
      "value": 191893,
      "link": "month/2020-02/sr-funnel/success-vs-failure/success-vs-failure",
    },
    { "name": "Records Sent", "value": 187349 },
  ]
index: 2
---

The data was collected from **Splunk** with the following query, and the date range was **1st-29th February 2020**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | eval is_request=1
  | eval is_retrieve=if(isnotnull(ExtractTime),1,0)
  | dedup ConversationID
  | stats sum(is_request) as requests, sum(is_retrieve) as retrieves
  | addtotals
```
