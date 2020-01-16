---
layout: funnel
title:  "Requester View"
date: "2019-12-02 14:10:30 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": 475557, "link": "month/2019-11/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": 292750, "link": "month/2019-11/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": 212772, "link": "month/2019-11/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": 172885, "link": "month/2019-11/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - November 2019**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
