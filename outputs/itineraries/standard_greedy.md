# Itinerary: standard / greedy

_Generated 2026-04-23T01:23:31_

## Scenario
- **standard**: Reference case: 30 attractions, $200, 09:00-21:00 x 3 days.
- N attractions: 30 (seed 42)
- Budget: $200
- Days: 3
- Daily window: 09:00 - 21:00
- Planner: greedy

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 18 |
| Total cost | $200.00 |
| Remaining budget | $0.00 |
| Total satisfaction | 106.4 |
| Total visit minutes | 1230.0 |
| Total travel minutes | 230.0 |
| Travel ratio | 0.158 |
| Category diversity | 1.0 |
| Daily balance | 0.4 |
| Runtime (seconds) | 0.0233 |

## Day 1
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:03 - 09:48 | Victory Bridge | landmark | $2 | 7.6 |
| 2 | 10:06 - 11:06 | Flower Market | market | $2 | 7.7 |
| 3 | 11:14 - 11:59 | Skyline Tower | landmark | $5 | 7.1 |
| 4 | 12:13 - 13:58 | Zen Garden | park | $3 | 8.0 |
| 5 | 14:03 - 15:03 | Lighthouse Point | landmark | $14 | 6.9 |
| 6 | 15:33 - 17:03 | Noodle House | restaurant | $25 | 7.8 |
| 7 | 17:10 - 17:55 | Fusion Kitchen | restaurant | $13 | 5.6 |
| 8 | 18:08 - 19:08 | Lakeside Park | park | $8 | 5.5 |
| 9 | 19:18 - 20:03 | Botanical Garden | park | $5 | 2.6 |

_Return to hotel at 20:20 (travel 17 min)._

## Day 2
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:07 - 09:52 | Craft Market | market | $3 | 5.6 |
| 2 | 09:55 - 12:10 | Modern Art Gallery | museum | $25 | 8.3 |
| 3 | 12:11 - 12:41 | Clock Tower | landmark | $12 | 4.3 |
| 4 | 12:55 - 13:55 | Science Center | museum | $33 | 6.4 |
| 5 | 14:01 - 16:31 | Concert Hall | entertainment | $27 | 8.2 |
| 6 | 16:46 - 17:46 | Old Cathedral | landmark | $7 | 5.3 |
| 7 | 17:59 - 18:59 | Riverside Park | park | $9 | 3.4 |

_Return to hotel at 19:14 (travel 15 min)._

## Day 3
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 09:05 - 10:50 | Hilltop Park | park | $6 | 4.2 |
| 2 | 11:03 - 11:33 | Spice Market | market | $1 | 1.9 |

_Return to hotel at 11:46 (travel 13 min)._
