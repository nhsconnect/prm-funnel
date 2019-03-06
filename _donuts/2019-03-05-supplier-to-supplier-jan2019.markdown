---
layout: donut
title:  "EHR Extracts sent grouped by sending and receiving system type"
date:   2019-03-05 15:46:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
datasource: NMS
categories: data
total: 325772
items: { "datasets":
            [{
                  "data": [
                        28422,
                        9199,
                        8718,
                        1510,
                        1420,
                        908,
                        413,
                        400,
                        148,
                        134,
                        116,
                        114,
                        100,
                        9,
                        4,
                        2
                  ],
                  "label": "Jan 19",
                  backgroundColor: [
                      "#5E42A6",
                      "#05C6F4",
                      "#05D7B3",
                      "#798B01",
                      "#BE7D03",
                      "#09090F",
                      "#2B252A",
                      "#6A2973",
                      "#F2AD85",
                      "#DB6D83",
                      "#FCFCFF",
                      "#E3D78D",
                      "#FF2626",
                      "#FF8A0C",
                      "#652773",
                      "#FDA099"
                  ],
                  label: 'Dataset 1'
            }],
            "labels": [
                  "EMIS -> EMIS",
                  "TPP -> EMIS",
                  "EMIS -> TPP",
                  "EMIS -> Vision",
                  "Vision -> EMIS",
                  "Vision -> Vision",
                  "TPP -> Vision",
                  "Vision -> TPP",
                  "TPP -> MT",
                  "EMIS -> MT",
                  "MT -> EMIS",
                  "MT -> TPP",
                  "MT -> MT",
                  "TPP -> TPP",
                  "Vision -> MT",
                  "MT -> Vision"
            ]
      }
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following query: 

```sql
index="spine2-live" 
      service=gp2gp 
      interactionID="urn:nhs:names:services:gp2gp/RCMR_IN010000UK05" 
            | stats  count by fromPName, toPName 
            | sort -count
```