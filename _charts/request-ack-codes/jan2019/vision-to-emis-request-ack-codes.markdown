---
layout: chart
title:  "Vision to EMIS RequestAckCodes"
date:   2019-03-22 16:25:00 +0000
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
            "#664422",
            "#900C3E"
          ]
labels: [
            "0 / 00: Success",
            "7: GP2GP messaging not enabled on this system",
            "10: Failed to successfully generate EHR extract",
            "20: Spine system responded with an error",
            "23: Message not sent because sending practice is not large message compliant",
            "30: Large Message general failure",
            "99: Undocumented error code",
            "None"
          ]
items: [
            154756,
            61,
            6,
            87,
            7,
            7,
            7,
            547
      ]
---
A chart representing the RequestAckCodes for messages from the sender to the requestor.

The data was collected from **Splunk** with the following query for the whole of **January 2019**:

This is the query that gave us information on the **RequestAckCode**, specifically where this maps **00** to **0**, as we have assumed all the 0s are a success.
```sql
index="gp2gp-mi" sourcetype="gppractice-SR"     
  | where ExtractFailurePoint=0 OR ExtractFailurePoint=60      
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
  | search SenderSupplier=EMIS
  | eval RequestAckCode=coalesce(RequestAckCode, RequestAckCode, "None")
  | eval RequestAckCode=if(RequestAckCode=="00","0",RequestAckCode)
  | stats dc(ConversationID) as count by SenderSupplier, RequestorSupplier, RequestAckCode 
  | sort RequestAckCode
```
