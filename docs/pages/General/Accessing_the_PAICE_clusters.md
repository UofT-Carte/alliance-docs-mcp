---
title: "Accessing the PAICE clusters"
url: "https://docs.alliancecan.ca/wiki/Accessing_the_PAICE_clusters"
category: "General"
last_modified: "2026-10-09T15:37:47Z"
page_id: 35053
display_title: "Accessing the PAICE clusters"
---

To run jobs or be granted large storage allocations (i.e. project and scratch), a user needs to belong to an AI project (AIP), and the PI responsible for that AIP must have a tier assigned to them. There are two methods for a PI to get a valid AIP. The first involves PIs that are affiliated with the three AI institutes (AMII, MILA, Vector). These have AIPs created for them by their home institutes, and are then added to the appropriate tier group to grant them preferential access to resources. An AIP can be created for a PI by navigating to that PI's role page and clicking Create AI project in the menu on the left. The PI must then be added to the aip-[clustername]-tier[1/2] group (the AI institute determines which group to add them to). This grants that PI, and any members of the AI project (aip-[PI-name]), storage and job access on that cluster, and also grants this access (at a tier 3 level, amounting to fewer resources and lower cluster priority) on the other two PAICE clusters.

The second way for a PI to gain resources on PAICE systems is if they are either researching AI without being affiliated with these three institutes, or if they are using AI in their (non-AI) research. The PI can create an AIP by first connecting to the CCDB and then clicking on Resources -> General Access to PAICE Systems, checking a box, and clicking the Submit button. This will create an AIP in their name and put them in the aip-tier3 or aip-tier4 group, which then gives them cluster resources and job submission access.

If a PI already has an AIP, but no tier assigned, they can still click one of these boxes to be granted tier 3 or tier 4 access; however, an AIP created for them with no tier assigned represents an admin error, as users will notice they have an AIP and yet still cannot use the clusters.

Note that users may have an AIP without having opted in to SSH access (via the first process described above); these are the several layers of configuration required to fully utilize the PAICE systems, and missing one leads to confusion and frustration for user and admin alike.