---
layout: funnel
title: "Requester View"
date: "2020-02-12 14:10:30 +0000"
datatype: Quantitative
confidence: Medium
datasource: NMS (gp2gp-mi)
categories: data
items:
  [
    {
      "name": "Registrations",
      "value": 439210,
      "link": "month/2020-02/rr-funnel/registrations/registrations",
    },
    {
      "name": "Transfers",
      "value": 270615,
      "link": "month/2020-02/rr-funnel/transfers/transfers",
    },
    {
      "name": "GP2GP",
      "value": 192875,
      "link": "month/2020-02/rr-funnel/gp2gp/gp2gp",
    },
    {
      "name": "Integrations",
      "value": 166737,
      "link": "month/2020-02/rr-funnel/integrations/integrations",
    },
  ]
index: 2
---

Data is sourced from **suppliers' data (MI) - February 2020**.

Values for each level of the funnel is the output of the following queries:

- [Registrations](registrations/registrations)
- [Transfers](transfers/transfers)
- [GP2GP](gp2gp/gp2gp)
- [Integrations](integrations/integrations) - Sum of suppressed and successfully integrated records
