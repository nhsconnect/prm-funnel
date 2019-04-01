---
layout: chart
title:  "Vision to EMIS ExtractAckCodes"
date:   2019-03-25 16:29:00 +0000
timeframe: Feb 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Requests Sent
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "0: Success",
    "value": 3887
  },
  {
    "name": "11: Failed to successfully integrate EHR Extract",
    "value": 3
  },
  {
    "name": "15: A-B-A EHR Extract Received and Stored As Suppressed Record",
    "value": 270
  },
  {
    "name": "17: A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
    "value": 2
  },
  {
    "name": "21: EHR Extract message not well-formed or not able to be processed",
    "value": 63
  },
  {
    "name": "28: Non A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
    "value": 2
  },
  {
    "name": "None",
    "value": 2876
  }
]
---
A chart representing the ExtractAckCodes for messages from the sender to the requestor.

The data was collected from **Splunk** with the following query for the whole of **February 2019**:

This is the query that gave us information on the **ExtractAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
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
  | eval RequestorSupplier=coalesce(RequestorSupplier, RequestorSupplier, "Unknown")     
  | rex field=SenderSoftware        
      "(?<SenderSupplier>.*)_(?<SenderSystem>.*)_(?<SenderVersion>.*)"     
  | lookup Spine2-NACS-Lookup NACS AS SenderODS OUTPUTNEW MName AS MName     
  | search RequestorSupplier=EMIS 
  | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "Unknown")     
  | search SenderSupplier=INPS 
  | eval ExtractAckCode=coalesce(ExtractAckCode, ExtractAckCode, "None")
  | eval ExtractAckCode=if(ExtractAckCode=="00","0",ExtractAckCode)
  | stats dc(ConversationID) as count by ExtractAckCode 
  | sort ExtractAckCode
```
