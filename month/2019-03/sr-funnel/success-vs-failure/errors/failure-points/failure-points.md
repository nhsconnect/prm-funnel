---
layout: chart
title:  "Request Failure Points"
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
          { name: 'Patient look-up', value: 202 },
          { name: 'PDS comparison with Requestor', value: 35 },
          { name: 'Requestor not large message compliant', value: 3440 },
          { name: 'Send record', value: 1525 },
          { name: 'Manually send duplicate record', value: 12 }
    ]
---
The total of extract failure points differ from the total requests received by ~20 data points. This is due to retries that eventually succeeded.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR" | stats  dc(ConversationID) as Requests by ExtractFailurePoint 
```

The extract failure point *PDS comparison with Requestor* has *RequestAckCodes* of *Sender check indicates that Requestor is not the patient’s current healthcare provider* as well as *Sender check indicates that Requestor is not the patient’s current healthcare provider*. This means the failure could happen due to either one of those reasons.
