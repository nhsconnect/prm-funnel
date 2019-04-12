---
layout: chart
title:  "Request Failure Error Codes"
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
        { name: 'Not specified', value: 4271 },
        { name: '20: Spine system responded with an error', value: 826 },
        { name: '303: Message size exceeds maximum message size allowed (TMS)', value: 13 },
        { name: '-31', value: 6 },
        { name: '-3', value: 1 }
    ]
---
To get a view on the failure points, please click [here](/prm-funnel/charts/2019-03/sender/extract-failure-points.html).
The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR"
    | where isnotnull(ExtractFailureType)
    | eval ExtractFailureErrorCode=coalesce(ExtractFailureErrorCode, ExtractFailureErrorCode, "Not specified")
    | stats dc(ConversationID)  by ExtractFailureErrorCode
```
