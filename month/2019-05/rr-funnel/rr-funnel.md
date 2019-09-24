---
layout: funnel
title:  "Requester View"
date: "2019-09-20 11:46:00 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items: [
    { "name": "Registrations", "value": 420178, "link": "month/2019-05/rr-funnel/registrations/registrations" },
    { "name": "Transfers", "value": 256290, "link": "month/2019-05/rr-funnel/transfers/transfers" },
    { "name": "GP2GP", "value": 186594, "link": "month/2019-05/rr-funnel/gp2gp/gp2gp" },
    { "name": "Integrations", "value": 155197, "link": "month/2019-05/rr-funnel/integrations/integrations" }
]
index: 2
---

Data is sourced from **suppliers' data (MI) - May 2019**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
