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
          { name: 'Requestor not large message compliant', value: 3436 },
          { name: 'Unknown', value: 1554 },
          { name: 'Patient Lookup', value: 202 },
          { name: 'Requestor is not the current healthcare provider of the patient', value: 26 },
          { name: 'Manual GP2GP retry', value: 12 },
          { name: 'PDS comparison with Requestor', value: 8 }
    ]
---
The data was collected from **Splunk** with the following query, and the date range was **1st-31st March 2019**:

```sql
index="gp2gp-mi" sourcetype="gppractice-SR" 
  | eval ExtractFailurePoint=coalesce(ExtractFailurePoint, -1)
  | eval ExtractFailureType=coalesce(ExtractFailureType, -1)
  | dedup ConversationID
  | eval RequestAckCode=tonumber(RequestAckCode) 
  | eval failurereason=case(
      ExtractFailurePoint==0 AND RequestAckCode != 0, "Unknown",
      ExtractFailurePoint==60, "Unknown",
      ExtractFailurePoint==10, "Patient Lookup",
      RequestAckCode==19, "Requestor is not the current healthcare provider of the patient",
      ExtractFailurePoint==20, "PDS comparison with Requestor",
      ExtractFailurePoint==50, "Requestor not large message compliant",
      ExtractFailurePoint==70, "Manual GP2GP retry",
      1=1, "other"
  )
  | where RequestAckCode != 0 OR ExtractFailurePoint != 0
  | stats count by failurereason
  | sort -count
```
