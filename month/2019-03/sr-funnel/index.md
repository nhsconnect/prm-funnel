---
layout: funnel
title:  "March 2019 Sender View"
date:   2019-04-05 15:46:00 +0000
datatype: Quantitative
confidence: Medium
datasource: NMS
categories: data
items: [
    { "name": "Requests Received", "value": 194762, "link": "charts/2019-03/sender/extract-success-vs-failures"},
    { "name": "Records Sent", "value": 189805 }
]
---
Splunk query to retrieve requests received:
```sql
index="gp2gp-mi" sourcetype="gppractice-SR" 
  | stats dc(ConversationID)
```

Splunk query to retrieve records sent:
```sql
index="gp2gp-mi" sourcetype="gppractice-SR" 
  | where isnotnull(ExtractTime) 
  | stats dc(ConversationID)
```