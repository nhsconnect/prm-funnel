---
layout: donut
title:  "EHR Extracts sent grouped by sending and receiving system type"
date:   2019-03-05 15:46:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Low
datasource: NMS
categories: data
total: 247499
chart_type: horizontalBar
colours: [
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
            "#F45F42",
            "#E3D78D",
            "#FF2626",
            "#FF8A0C",
            "#652773",
            "#FDA099"
          ]
labels: [
            "EMIS -> EMIS",
            "TPP -> TPP",
            "TPP -> EMIS",
            "EMIS -> TPP",
            "EMIS -> Vision",
            "Vision -> EMIS",
            "Vision -> Vision",
            "TPP -> Vision",
            "Vision -> TPP",
            "TPP -> MT",
            "MT -> TPP",
            "MT -> EMIS",
            "EMIS -> MT",
            "MT -> MT",
            "Vision -> MT",
            "MT -> Vision"
          ]
items: [
            138176,
            115836,
            43707,
            40617,
            7761,
            6781,
            3648,
            2312,
            1680,
            609,
            600,
            589,
            580,
            349,
            22,
            20
      ]
percentages: [
            56,
            bla,
            18,
            16,
            3,
            3,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
      ]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries:

This is the query that gave us all the supplier to supplier system data except for TPP -> TPP transfers.
```sql
index="spine2-live" 
      service=gp2gp 
      interactionID="urn:nhs:names:services:gp2gp/RCMR_IN010000UK05" 
            | dedup conversationID 
            | stats count by fromPName, toPName
            | eventstats sum(count) as totalCount
            | eval percentage=round(count/totalCount * 100, 0)
            | table fromPName, toPName, count, percentage, totalCount
            | sort -count
```

This query informed our TPP -> TPP transfer data.
```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
            | lookup GP2GP-Practice-Lookup PracticeCode AS RequestorODS OUTPUTNEW CurrentClinicalSupplier AS RequestorSystem
            | lookup GP2GP-Practice-Lookup PracticeCode AS SenderODS OUTPUTNEW CurrentClinicalSupplier AS SenderSystem
            | where SenderSystem="TPP"
            | stats count by SenderSystem, RequestorSystem
            | sort - count
```
