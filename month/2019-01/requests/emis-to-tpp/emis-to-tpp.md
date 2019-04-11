---
layout: chart
title:  "EMIS to TPP ExtractAckCodes"
date:   2019-03-22 16:26:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Requests Sent
datasource: NMS (gp2gp-mi)
categories: data
items: [ 
          { name: '0: Success', value: 34565 },
          { name: '11: Failed to successfully integrate EHR Extract',
            value: 21 },
          { name: '12: Duplicate EHR Extract received', value: 30 },
          { name: '15: A-B-A EHR Extract Received and Stored As Suppressed Record',
            value: 3007 },
          { name: '17: A-B-A EHR Extract Received and rejected due to wrong record or wrong patient',
            value: 47 },
          { name: '25: Large messages rejected due to timeout duration reached of overall transfer',
            value: 16 },
          { name: '26: Returning Patient EHR Extract Received and filed as an attachment',
            value: 2 },
          { name: '28: Non A-B-A EHR Extract Received and rejected due to wrong record or wrong patient',
            value: 22 },
          { name: '31: The overall EHR Extract has been rejected because one or more attachments via Large Messages were not received',
            value: 1 } 
    ]
---
A chart representing the ExtractAckCodes for messages from the sender to the requestor.

The data was collected from **Splunk** with the following query for the whole of **January 2019**:

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
