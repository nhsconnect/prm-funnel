---
layout: chart
title:  "EMIS to TPP ExtractAckCodes"
date: "2019-03-23 16:26:00 +0000"
timeframe: Dec 2018
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Requests Sent
datasource: NMS (gp2gp-mi)
categories: data
items: [
  {
    "name": "0: Success",
    "value": 22127
  },
  {
    "name": "11: Failed to successfully integrate EHR Extract",
    "value": 40
  },
  {
    "name": "12: Duplicate EHR Extract received",
    "value": 367
  },
  {
    "name": "17: A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
    "value": 3
  },
  {
    "name": "28: Non A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
    "value": 34
  },
  {
    "name": "30: Large Message general failure",
    "value": 226
  },
  {
    "name": "31: The overall EHR Extract has been rejected because one or more attachments via Large Messages were not received",
    "value": 13
  },
  {
    "name": "99: Unexpected condition",
    "value": 3
  },
  {
    "name": "None",
    "value": 7706
  }
]
---
A chart representing the ExtractAckCodes for messages from the sender to the requestor.

The data was collected from **Splunk** with the following query for the whole of **December 2018**:

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
  | search RequestorSupplier=TPP 
  | eval SenderSupplier=coalesce(SenderSupplier, SenderSupplier, MName, MName, "Unknown")     
  | search SenderSupplier=EMIS 
  | eval ExtractAckCode=coalesce(ExtractAckCode, ExtractAckCode, "None")
  | eval ExtractAckCode=if(ExtractAckCode=="00","0",ExtractAckCode)
  | stats dc(ConversationID) as count by ExtractAckCode 
  | sort ExtractAckCode
```
