---
layout: chart
title:  "Large message details"
date:   2019-03-05 15:46:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
datasource: NMS
categories: data
total: 1234
chart_type: doughnut
colours: [
            "#5E42A6",
            "#05C6F4",
            "#F2AD85",
            "#DB6D83",
            "#F45F42"
          ]
labels: [
            "Success",
            "JDI 1",
            "JDI 2",
            "JDI 3",
            "JDI 4"
          ]
items: [
            1000,
            200,
            30,
            2,
            2
      ]
---
A chart representing the details of Large messages.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st January 2019:

This is the query that gave us information on what is classed as a large message
```sql
 INSERT
```

This query informed our TPP -> TPP transfer data.
```sql
INSERT
```
