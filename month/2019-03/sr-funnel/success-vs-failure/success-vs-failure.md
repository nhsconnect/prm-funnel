---
layout: chart
title:  "Request Success Vs Failure"
date:   2019-03-20 12:28:00 +0000
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
        { name: 'Succeeded', value: 189661 },
        { name: 'Failed', value: 5117, link: "month/2019-03/sr-funnel/success-vs-failure/errors/errors" }
    ]
---
[To get a view on the failure points, please click here](/prm-funnel/month/2019-03/sr-funnel/success-vs-failure/errors/failure-points/failure-points.html).

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR" 
  | eval success_status = if(isnull(ExtractFailureType), "Succeeded", "Failed")
  | stats dc(ConversationID) as Requests by success_status
```