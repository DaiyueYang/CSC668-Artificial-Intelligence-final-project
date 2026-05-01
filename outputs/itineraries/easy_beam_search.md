# Itinerary: easy / beam_search

_Generated 2026-04-23T01:23:31_

## Scenario
- **easy**: Larger budget, longer day window, fewer attractions.
- N attractions: 20 (seed 42)
- Budget: $400
- Days: 3
- Daily window: 08:00 - 22:00
- Planner: beam_search (beam_width=5)

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 20 |
| Total cost | $352.00 |
| Remaining budget | $48.00 |
| Total satisfaction | 116.3 |
| Total visit minutes | 1680.0 |
| Total travel minutes | 302.5 |
| Travel ratio | 0.153 |
| Category diversity | 1.0 |
| Daily balance | 0.62 |
| Runtime (seconds) | 0.1632 |

## Day 1
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:00 - 09:45 | Old Cathedral | landmark | $4 | 8.5 |
| 2 | 09:50 - 11:05 | Zen Garden | park | $1 | 8.4 |
| 3 | 11:21 - 12:21 | Victory Bridge | landmark | $10 | 9.8 |
| 4 | 12:31 - 13:31 | Noodle House | restaurant | $12 | 8.1 |
| 5 | 13:38 - 14:53 | Riverside Park | park | $2 | 7.1 |
| 6 | 15:20 - 16:50 | Hilltop Park | park | $10 | 7.5 |
| 7 | 16:57 - 17:57 | Skyline Tower | landmark | $4 | 5.0 |
| 8 | 18:10 - 19:25 | Fusion Kitchen | restaurant | $23 | 7.2 |
| 9 | 19:44 - 20:59 | Harbor Grill | restaurant | $12 | 1.8 |

_Return to hotel at 21:16 (travel 17 min)._

## Day 2
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 08:15 - 09:00 | Night Bazaar | market | $0 | 4.2 |
| 2 | 10:00 - 11:30 | War Memorial Museum | museum | $24 | 7.0 |
| 3 | 11:35 - 12:20 | Old Town Market | market | $1 | 3.7 |
| 4 | 12:38 - 13:38 | City History Museum | museum | $24 | 6.0 |
| 5 | 13:42 - 15:27 | Modern Art Gallery | museum | $21 | 5.0 |
| 6 | 15:36 - 17:51 | Comedy Theater | entertainment | $57 | 8.5 |
| 7 | 18:12 - 19:27 | Botanical Garden | park | $6 | 2.2 |

_Return to hotel at 19:38 (travel 11 min)._

## Day 3
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 08:17 - 08:47 | Flower Market | market | $2 | 1.7 |
| 2 | 10:00 - 11:15 | Science Center | museum | $31 | 4.4 |
| 3 | 11:31 - 15:01 | Adventure World | entertainment | $36 | 3.2 |
| 4 | 15:03 - 18:18 | City Aquarium | entertainment | $72 | 7.0 |

_Return to hotel at 18:29 (travel 11 min)._
