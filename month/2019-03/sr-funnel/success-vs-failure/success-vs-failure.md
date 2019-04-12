---
layout: chart
title:  "Request Success vs Failure"
date: "2019-03-20 12:28:00 +0000"
timeframe: March 2019
datatype: Quantitative
confidence: Medium
funnel_slice: Requests Received
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  options:
    legend:
      position: "bottom"
      
items: [ 
        { name: 'Succeeded', value: 189066 },
        { name: 'Failed', value: 5211, link: "month/2019-03/sr-funnel/success-vs-failure/errors/failure-points/failure-points" }
    ]
---
The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
  | eval ExtractFailurePoint=coalesce(ExtractFailurePoint, ExtractFailurePoint, -1)
  | eval success=case(ExtractFailurePoint==0 AND RequestAckCode==0, "success", ExtractFailurePoint != 0, "failure")
  | stats dc(ConversationID) by success
```
