---
layout: funnel
title:  "Requester View"
date: "2019-10-02 11:59:53"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": 454445, "link": "month/2019-08/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": 286131, "link": "month/2019-08/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": 210999, "link": "month/2019-08/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": 170180, "link": "month/2019-08/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - August 2019**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
