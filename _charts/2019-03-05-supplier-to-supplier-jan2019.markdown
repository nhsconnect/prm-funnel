---
layout: chart
title:  "EHR Requests sent grouped by sending and receiving system type"
date:   2019-03-05 15:46:00 +0000
funnel_slice: EHR Requests Sent
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
            "EMIS -> TPP",
            "TPP -> EMIS",
            "INPS -> EMIS",
            "INPS -> TPP",
            "EMIS -> INPS",
            "Microtest -> EMIS",
            "EMIS -> Unknown",
            "Microtest -> TPP",
            "Unknown -> EMIS",
            "TPP -> INPS",
            "INPS -> INPS",
            "EMIS -> Microtest",
            "TPP -> TPP",
            "Unknown -> TPP",
            "ISOFT -> EMIS",
            "EMIS -> ISOFT",
            "TPP -> Unknown",
            "TPP -> Microtest",
            "Microtest -> Microtest",
            "ISOFT -> TPP",
            "INPS -> Unknown",
            "INPS -> Microtest",
            "TPP -> ISOFT",
            "Microtest -> INPS",
            "INPS -> ISOFT",
            "Unknown -> Unknown",
            "Unknown -> INPS",
            "Unknown -> Microtest",
            "Microtest -> ISOFT",
            "Microtest -> Unknown",
            "ISOFT -> ISOFT"
          ]
items: [
            134032,
            41824,
            38888,
            8702,
            2730,
            1344,
            721,
            706,
            653,
            573,
            337,
            334,
            228,
            220,
            155,
            95,
            88,
            88,
            78,
            71,
            21,
            18,
            17,
            16,
            10,
            7,
            5,
            2,
            2,
            1,
            1,
            0
      ]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st January 2019:

```sql
index="gp2gp-mi" sourcetype="gppractice-RR"
            | lookup GP2GP-Practice-Lookup PracticeCode 
                  AS RequestorODS OUTPUTNEW CurrentClinicalSupplier
                  AS RequestorSystem
            | lookup GP2GP-Practice-Lookup PracticeCode 
                  AS SenderODS OUTPUTNEW CurrentClinicalSupplier
                  AS SenderSystem
            | stats dc(ConversationID) as count by SenderSystem, RequestorSystem
            | sort - count
```
