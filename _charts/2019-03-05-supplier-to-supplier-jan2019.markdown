---
layout: chart
title:  "EHR Requests sent grouped by sending and receiving system type"
date: "2019-03-05 15:46:00 +0000"
funnel_slice: EHR Requests Sent
timeframe: Jan 2019
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
          { "name": "EMIS -> EMIS", "value": 138679, "link": "charts/extract-ack-codes/jan2019/emis-to-emis-extract-ack-codes"},
          { "name": "EMIS -> TPP", "value": 40375, "link": "charts/extract-ack-codes/jan2019/emis-to-tpp-extract-ack-codes" },
          { "name": "TPP -> EMIS", "value": 7778, "link": "charts/extract-ack-codes/jan2019/tpp-to-emis-extract-ack-codes" },      
          { "name": "Vision -> EMIS", "value": 2283, "link": "charts/extract-ack-codes/jan2019/vision-to-emis-extract-ack-codes" },
          { "name": "Vision -> TPP", "value": 608, "link": "charts/extract-ack-codes/jan2019/microtest-to-emis-extract-ack-codes" },
          { "name": "MicroTest -> TPP", "value": 16, "link": "charts/extract-ack-codes/jan2019/microtest-to-tpp-extract-ack-codes" },
          { "name": "MicroTest -> EMIS", "value": 581, "link": "charts/extract-ack-codes/jan2019/tpp-to-tpp-extract-ack-codes" },
          { "name": "TPP -> TPP", "value": 61, "link": "charts/extract-ack-codes/jan2019/emis-to-unknown-extract-ack-codes8"  }        
        ]
---
A chart representing the EHR Sent Requests split into source and target system.

The data was collected from **Splunk** with the following queries, and the date range was 1st-31st January 2019:

```sql
 index="gp2gp-mi" sourcetype="gppractice-RR"
    | where RequestFailurePoint=0 OR RequestFailurePoint=60 
    | join type=outer RequestorODS 
      [search index="gp2gp-mi" sourcetype="gppractice-HR"] 
    | join type=outer SenderODS 
        [search index="gp2gp-mi" sourcetype="gppractice-HR" 
          | rename RequestorODS as SenderODS 
          | rename RequestorSoftware as SenderSoftware]
    | rex field=RequestorSoftware 
      "(?<RequestorSupplier>.*)_(?<RequestorSystem>.*)_(?<RequestorVersion>.*)"
    | eval RequestorSupplier=coalesce(RequestorSupplier, RequestorSupplier, "unknown")
    | rex field=SenderSoftware 
      "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"
    | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName
    | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "unknown")
    | stats dc(ConversationID) as count by SenderSupplier, RequestorSupplier
    | sort - count
```
