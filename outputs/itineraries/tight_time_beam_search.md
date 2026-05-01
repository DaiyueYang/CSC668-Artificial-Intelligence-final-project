# Itinerary: tight_time / beam_search

_Generated 2026-04-23T01:23:31_

## Scenario
- **tight_time**: Short daily window 10:00-17:00 - time is the binding constraint.
- N attractions: 30 (seed 42)
- Budget: $200
- Days: 3
- Daily window: 10:00 - 17:00
- Planner: beam_search (beam_width=5)

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 14 |
| Total cost | $163.00 |
| Remaining budget | $37.00 |
| Total satisfaction | 94.6 |
| Total visit minutes | 1020.0 |
| Total travel minutes | 213.5 |
| Travel ratio | 0.173 |
| Category diversity | 1.0 |
| Daily balance | 0.88 |
| Runtime (seconds) | 0.187 |

## Day 1
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 10:03 - 10:48 | Victory Bridge | landmark | $2 | 7.6 |
| 2 | 11:05 - 12:05 | Flower Market | market | $2 | 7.7 |
| 3 | 12:24 - 14:09 | Zen Garden | park | $3 | 8.0 |
| 4 | 14:24 - 15:08 | Skyline Tower | landmark | $5 | 7.1 |
| 5 | 15:12 - 16:42 | Rooftop Bistro | restaurant | $17 | 6.7 |

_Return to hotel at 16:57 (travel 15 min)._

## Day 2
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 10:05 - 12:20 | Modern Art Gallery | museum | $25 | 8.3 |
| 2 | 12:22 - 13:07 | Craft Market | market | $3 | 5.6 |
| 3 | 13:18 - 14:18 | Lighthouse Point | landmark | $14 | 6.9 |
| 4 | 14:32 - 15:32 | Old Cathedral | landmark | $7 | 5.3 |
| 5 | 15:45 - 16:30 | Fusion Kitchen | restaurant | $13 | 5.6 |

_Return to hotel at 16:52 (travel 22 min)._

## Day 3
| # | Window | Name | Category | Cost | Score |
|---|---|---|---|---|---|
| 1 | 10:11 - 12:41 | Concert Hall | entertainment | $27 | 8.2 |
| 2 | 13:09 - 14:09 | Lakeside Park | park | $8 | 5.5 |
| 3 | 14:16 - 15:46 | Noodle House | restaurant | $25 | 7.8 |
| 4 | 16:06 - 16:36 | Clock Tower | landmark | $12 | 4.3 |

_Return to hotel at 16:43 (travel 7 min)._
