# Itinerary: tight_budget / beam_search

_Generated 2026-04-23T01:23:31_

## Scenario
- **tight_budget**: Low budget - forces the planner toward cheap attractions.
- N attractions: 30 (seed 42)
- Budget: $80
- Days: 3
- Daily window: 09:00 - 21:00
- Planner: beam_search (beam_width=5)

## Metrics
| Metric | Value |
|---|---|
| Feasibility | OK |
| Attractions visited | 11 |
| Total cost | $80.00 |
| Remaining budget | $0.00 |
| Total satisfaction | 66.2 |
| Total visit minutes | 735.0 |
| Total travel minutes | 168.5 |
| Travel ratio | 0.186 |
| Category diversity | 0.83 |
| Daily balance | 0.04 |
| Runtime (seconds) | 0.1184 |

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
| 1 | 09:07 - 09:52 | Craft Market | market | $3 | 5.6 |
| 2 | 10:02 - 11:02 | Old Cathedral | landmark | $7 | 5.3 |
| 3 | 11:15 - 12:00 | Botanical Garden | park | $5 | 2.6 |
| 4 | 12:12 - 12:42 | Spice Market | market | $1 | 1.9 |

_Return to hotel at 12:54 (travel 13 min)._

## Day 3
_(rest day - no visits scheduled)_
