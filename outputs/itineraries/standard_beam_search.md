# Itinerary: standard / beam_search

_Generated 2026-04-23T01:23:31_

## Scenario
- **standard**: Reference case: 30 attractions, $200, 09:00-21:00 x 3 days.
- N attractions: 30 (seed 42)
- Budget: $200
- Days: 3
- Daily window: 09:00 - 21:00
- Planner: beam_search (beam_width=5)

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 19 |
| Total cost | $198.00 |
| Remaining budget | $2.00 |
| Total satisfaction | 110.4 |
| Total visit minutes | 1305.0 |
| Total travel minutes | 277.3 |
| Travel ratio | 0.175 |
| Category diversity | 1.0 |
| Daily balance | 0.67 |
| Runtime (seconds) | 0.2279 |

## Day 1
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:03 - 09:48 | Victory Bridge | landmark | $2 | 7.6 |
| 2 | 10:01 - 11:46 | Zen Garden | park | $3 | 8.0 |
| 3 | 12:05 - 13:05 | Flower Market | market | $2 | 7.7 |
| 4 | 13:13 - 13:58 | Skyline Tower | landmark | $5 | 7.1 |
| 5 | 14:02 - 15:32 | Rooftop Bistro | restaurant | $17 | 6.7 |
| 6 | 15:52 - 18:22 | Concert Hall | entertainment | $27 | 8.2 |
| 7 | 18:50 - 19:50 | Lakeside Park | park | $8 | 5.5 |

_Return to hotel at 20:09 (travel 19 min)._

## Day 2
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:05 - 11:20 | Modern Art Gallery | museum | $25 | 8.3 |
| 2 | 11:22 - 12:07 | Craft Market | market | $3 | 5.6 |
| 3 | 12:18 - 13:18 | Lighthouse Point | landmark | $14 | 6.9 |
| 4 | 13:32 - 14:32 | Old Cathedral | landmark | $7 | 5.3 |
| 5 | 14:50 - 16:20 | Noodle House | restaurant | $25 | 7.8 |
| 6 | 16:27 - 17:12 | Fusion Kitchen | restaurant | $13 | 5.6 |
| 7 | 17:38 - 18:53 | Harbor Grill | restaurant | $20 | 5.5 |
| 8 | 19:17 - 20:02 | Botanical Garden | park | $5 | 2.6 |

_Return to hotel at 20:19 (travel 17 min)._

## Day 3
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:05 - 10:50 | Hilltop Park | park | $6 | 4.2 |
| 2 | 10:59 - 11:29 | Clock Tower | landmark | $12 | 4.3 |
| 3 | 11:35 - 12:05 | Spice Market | market | $1 | 1.9 |
| 4 | 12:11 - 12:41 | Night Bazaar | market | $3 | 1.6 |

_Return to hotel at 12:53 (travel 12 min)._
