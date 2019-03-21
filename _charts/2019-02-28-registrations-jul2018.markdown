---
layout: chart
title:  "Type of Patient Transfer"
date:   2019-03-02 15:46:00 +0000
funnel_slice: Registrations
timeframe: Jul 2018
datatype: Quantitative
confidence: Medium
datasource: GP2GP Utilisation Report
categories: data
total: 325772
chart_type: doughnut
items: [
            200747,
            64198,
            60827
       ]
colours: [
          "red",
          "blue",
          "#FFC4AA"
         ]
labels: [
          "GP2GP",
          "TPP Internal",
          "Unknown"
        ]
---
A chart representing the percentage of types of patient transfer that occurred.

At the moment, "Unknown" represents a group that includes (but may not be limited to):
- Births (where there is no data to migrate)
- Those who have never had a Primary Care registration before (where there is no data to migrate)
- Those who have had a Primary Care registration before (where there is data to migrate but no known data migration has happened)

At the moment, we cannot distinguish between these groups who make up "Unknown".
