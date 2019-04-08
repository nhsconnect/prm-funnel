---
layout: chart
title:  "GP2GP errors"
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
          { name: 'No Failure', value: 189569 },
          { name: 'Patient look-up', value: 202 },
          { name: 'PDS comparison with Requestor', value: 35 },
          { name: 'SDS lookup for Large Message support', value: 3440 },
          { name: 'Send EHR', value: 1525 },
          { name: 'Manually Send duplicate EHR', value: 12 }
    ]
---
The total of extract failure points differ from the total requests received by ~20 data points. This is due to retries that eventually succeeded, however.

The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR" | stats  dc(ConversationID) as Requests by ExtractFailurePoint 
```