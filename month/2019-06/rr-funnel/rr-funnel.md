---
layout: funnel
title:  "Requester View"
date: "2019-09-25 11:59:53"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": 404007, "link": "month/2019-06/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": 253350, "link": "month/2019-06/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": 182149, "link": "month/2019-06/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": 147973, "link": "month/2019-06/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - June 2019**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
