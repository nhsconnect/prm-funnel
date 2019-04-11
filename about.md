---
layout: page
title: About
permalink: /about/
---
This site visualises data collated from the GP2GP Utilisation Report (July 2018), data from GP practice clinical suppliers (the MI dataset) as loaded into the NMS Trends 'gp2gp-mi' index and data about messages sent over the NHS Spine recorded in the NMS Trends 'spine2-live' index.

The PRM team does not have a 100% reliable source of information about the clinical supplier for each GP practice over time.  For suppliers that provide MI information we can deduce the current clinical supplier based on the system reporting the MI data (with the caveat that this may not be accurate if a GP practice is running multiple systems as part of a process of transitioning suppliers).  For other cases static lookup tables are used which do not track suppliers over time.

The information presented is mainly gathered from the MI data. The PRM team have a good-degree of confidence in this data as:
1. Approximately, 89% of GP practices provide this data.
2. Between 99-100% of GP practices that provide this data, provide it every day.
3. For patient registrations that result in a GP2GP interaction, there is a high correlation between the data reported by the MI data and the data recorded by the NHS Spine.
4. Approximately, 92% of GP2GP interactions involve a system that reports MI data.

Information about the 11% of GP practices that do not provide MI data (and 8% of GP2GP interactions) is obtained from messages sent over Spine.

Registration data before March 2019 is returned from the GP2GP utilisation report (which obtains data from NHAIS and other data-sources which the PRM team does not currently have access to).  The data is from July 2018 as that is the most recent report currently available. From March 2019 onwards, registration data is retrieved from the MI dataset.

