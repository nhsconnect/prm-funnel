---
layout: funnel
title:  "Requester View"
date: "<Timestamp>"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": <Total registrations>, "link": "month/<Year-Month-Directory>/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": <Total transfers>, "link": "month/<Year-Month-Directory>/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": <Total GP2GP>, "link": "month/<Year-Month-Directory>/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": <Total integrations>, "link": "month/<Year-Month-Directory>/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - <Month> <Year>**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
