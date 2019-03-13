---
layout: chart
title:  "EHR extracts grouped by message type"
date:   2019-03-05 15:46:00 +0000
funnel_slice: EHR Extracts
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
datasource: NMS
categories: data
total: 1234
chart_type: doughnut
colours: [
            "#5E42A6",
            "#05C6F4"
          ]
labels: [
            "Large Messages",
            "Small Messages"
          ]
items: [
            138176,
            115836
      ]
---
A chart representing the EHR Extracts split into message types.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st January 2019:

This is the query that gave us information on what is classed as a large message
```sql
 INSERT
```

This query informed our TPP -> TPP transfer data.
```sql
INSERT
```
