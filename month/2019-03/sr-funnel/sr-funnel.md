---
layout: funnel
title:  "Sender View"
date: "2019-04-05 15:46:00 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS
categories: data
items: [
    { "name": "Requests Received", "value": 196009, "link": "month/2019-03/sr-funnel/success-vs-failure/success-vs-failure"},
    { "name": "Records Sent", "value": 191032 }
]
index: 2
---
```sql
index="gp2gp-mi" sourcetype="gppractice-SR" 
  | eval is_request=1
  | eval is_retrieve=if(isnotnull(ExtractTime),1,0)
  | dedup ConversationID
  | stats sum(is_request) as requests, sum(is_retrieve) as retrieves
  | addtotals
```
