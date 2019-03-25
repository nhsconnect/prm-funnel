---
layout: chart
title:  "TPP to EMIS ExtractAckCodes"
date:   2019-03-22 16:27:00 +0000
timeframe: Jan 2019
datatype: Quantitative
confidence: Medium
funnel_slice: EHR Requests Sent
datasource: NMS (gp2gp-mi)
categories: data
chart_config: 
  type: 'doughnut'
colours: [
            "#FF6DA7",
            "#E8A333",
            "#4E8516",
            "#27DEE8",
            "#A35EFF",
            "#571845",
            "#900C3E",
            "#FF5733",
            "#FFC300"
          ]
labels: [
            "0: Success",
            "11: Failed to successfully integrate EHR Extract",
            "12: Duplicate EHR Extract received",
            "15: A-B-A EHR Extract Received and Stored As Suppressed Record",
            "17: A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
            "25: Large messages rejected due to timeout duration reached of overall transfer",
            "26: Returning Patient EHR Extract Received and filed as an attachment",
            "28: Non A-B-A EHR Extract Received and rejected due to wrong record or wrong patient",
            "31: The overall EHR Extract has been rejected because one or more attachments via Large Messages were not received"
          ]
items: [
            34566,
            21,
            30,
            3007,
            45,
            16,
            2,
            22,
            1
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
  | eval ExtractAckCode=if(ExtractAckCode=="00","0",ExtractAckCode)
  | stats dc(ConversationID) as count by ExtractAckCode 
  | sort ExtractAckCode
```
