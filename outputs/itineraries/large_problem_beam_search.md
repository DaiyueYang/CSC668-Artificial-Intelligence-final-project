# Itinerary: large_problem / beam_search

_Generated 2026-04-23T01:23:34_

## Scenario
- **large_problem**: Scaled up: 50 attractions, 5 days - tests scalability.
- N attractions: 50 (seed 42)
- Budget: $400
- Days: 5
- Daily window: 09:00 - 21:00
- Planner: beam_search (beam_width=10)

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 37 |
| Total cost | $387.00 |
| Remaining budget | $13.00 |
| Total satisfaction | 226.5 |
| Total visit minutes | 2355.0 |
| Total travel minutes | 554.9 |
| Travel ratio | 0.191 |
| Category diversity | 1.0 |
| Daily balance | 0.65 |
| Runtime (seconds) | 2.2351 |

## Day 1
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:07 - 10:07 | Old Cathedral | landmark | $1 | 9.6 |
| 2 | 10:13 - 11:13 | Lakeside Park | park | $7 | 8.5 |
| 3 | 11:24 - 11:54 | Victory Bridge 4 | landmark | $3 | 9.0 |
| 4 | 12:09 - 13:09 | Victory Bridge | landmark | $2 | 9.1 |
| 5 | 13:19 - 14:34 | Harbor Grill | restaurant | $12 | 8.3 |
| 6 | 14:59 - 15:59 | Skyline Tower 2 | landmark | $3 | 7.8 |
| 7 | 16:10 - 18:10 | Botanical Garden 4 | park | $1 | 7.1 |
| 8 | 18:28 - 19:28 | Lighthouse Point | landmark | $8 | 7.2 |
| 9 | 19:46 - 20:46 | Hilltop Park | park | $1 | 6.1 |

_Return to hotel at 20:58 (travel 13 min)._

## Day 2
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:10 - 10:10 | Old Town Market | market | $1 | 6.4 |
| 2 | 10:25 - 11:10 | Botanical Garden | park | $2 | 6.7 |
| 3 | 11:27 - 12:27 | Night Bazaar | market | $1 | 6.0 |
| 4 | 12:33 - 13:18 | Old Cathedral 3 | landmark | $6 | 6.5 |
| 5 | 13:20 - 14:05 | Flower Market | market | $0 | 5.4 |
| 6 | 14:33 - 16:33 | Natural History Museum | museum | $33 | 8.8 |
| 7 | 16:56 - 17:56 | Noodle House | restaurant | $15 | 7.2 |
| 8 | 18:07 - 19:07 | Fusion Kitchen 2 | restaurant | $24 | 8.1 |
| 9 | 19:15 - 20:00 | Zen Garden 3 | park | $5 | 5.2 |

_Return to hotel at 20:05 (travel 5 min)._

## Day 3
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:09 - 09:54 | Night Bazaar 3 | market | $2 | 4.7 |
| 2 | 10:10 - 11:10 | Flower Market 4 | market | $3 | 4.8 |
| 3 | 11:22 - 12:07 | Skyline Tower | landmark | $12 | 5.6 |
| 4 | 12:22 - 14:37 | War Memorial Museum 5 | museum | $26 | 7.6 |
| 5 | 14:50 - 15:50 | Riverside Park | park | $9 | 5.0 |
| 6 | 16:13 - 18:43 | City Aquarium | entertainment | $38 | 7.8 |
| 7 | 19:00 - 20:00 | Harbor Grill 3 | restaurant | $27 | 7.1 |

_Return to hotel at 20:12 (travel 12 min)._

## Day 4
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:06 - 10:21 | Spice Market | market | $2 | 4.0 |
| 2 | 10:38 - 11:38 | War Memorial Museum | museum | $20 | 6.5 |
| 3 | 11:42 - 12:42 | Clock Tower | landmark | $10 | 4.7 |
| 4 | 12:47 - 13:32 | Hilltop Park 5 | park | $1 | 3.0 |
| 5 | 13:40 - 14:40 | Zen Garden | park | $9 | 4.2 |
| 6 | 14:49 - 15:34 | Noodle House 4 | restaurant | $29 | 7.0 |
| 7 | 15:37 - 16:52 | Riverside Park 2 | park | $1 | 2.4 |
| 8 | 17:14 - 17:59 | Fusion Kitchen | restaurant | $30 | 6.7 |
| 9 | 18:23 - 19:23 | Rooftop Bistro | restaurant | $12 | 1.9 |

_Return to hotel at 19:37 (travel 14 min)._

## Day 5
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 10:00 - 11:00 | City History Museum | museum | $23 | 5.9 |
| 2 | 11:25 - 11:55 | Craft Market | market | $4 | 2.6 |
| 3 | 12:10 - 13:10 | Old Town Market 2 | market | $4 | 2.0 |

_Return to hotel at 13:19 (travel 9 min)._
