# Speech Script: AI-Based Constrained Travel Itinerary Planning

## Part 1. Opening

Good morning everyone.

Today I will introduce my project, **AI-Based Constrained Travel Itinerary Planning**. This project studies how to automatically generate a feasible multi-day travel itinerary under realistic constraints.
The key idea is that a good itinerary should be both satisfying for the traveler and feasible in practice.

## Part 2. Why This Problem Matters

Travel planning is not just about picking the most attractive places. Travelers must also consider budget, daily available time, attraction opening hours, travel time, and waiting time. Because these factors interact with each other, itinerary planning becomes a meaningful AI search and decision-making problem.
This means the problem is not only about preference, but also about scheduling and resource allocation.

## Part 3. Problem Definition

The goal of the system is to produce a feasible multi-day itinerary that maximizes total satisfaction. In this project, total satisfaction is defined as the sum of the priority scores of all visited attractions.
So the system has to balance quality and feasibility at the same time.

## Part 4. Inputs

The system takes three main inputs. The first is a set of attractions, and each attraction has an ID, category, cost, visit duration, opening and closing times, coordinates, and a priority score. The second is a travel-time matrix that includes both the attractions and a hotel node. The third is the trip configuration, including total budget, number of days, daily start and end time, and maximum waiting time.
These inputs together define both what the traveler wants and what the planner is allowed to do.

## Part 5. Constraints

The planner must satisfy several hard constraints. It must stay within budget, every visit must finish before the attraction closes, waiting time cannot exceed the allowed limit, the traveler must be able to return to the hotel before the end of each day, and the same attraction cannot be visited twice.
These constraints are important because even a high-scoring itinerary is useless if it cannot actually be followed.

## Part 6. Dataset Design

To keep the experiments reproducible, I used synthetic data instead of real travel APIs. The dataset contains six attraction categories: museum, park, restaurant, landmark, market, and entertainment. Each category has different patterns for cost, duration, and opening hours. Attractions are also generated around cluster centers to imitate city districts, and travel time is computed from Euclidean distance using a fixed travel speed.
This gives the project a controlled setting while still preserving realistic trade-offs between distance, time, and attraction value.

## Part 7. Greedy Baseline

The first planning method is a greedy baseline. At each step, it selects the best currently feasible attraction using a composite score based on priority, time efficiency, and cost efficiency. This method is fast and simple, but it only looks one step ahead, so it can miss better global solutions.
Its advantage is that it is easy to understand, easy to implement, and efficient enough to serve as a strong baseline.

## Part 8. Beam Search

The second method is beam search. Instead of keeping only one partial itinerary, it keeps the top `K` partial solutions at the same time. It scores them using satisfaction, number of visits, travel efficiency, category diversity, and remaining budget. This makes beam search less myopic and usually stronger than the greedy baseline.
Because it explores multiple promising directions in parallel, it can avoid some poor early choices that the greedy method cannot recover from.

## Part 9. Experimental Setup

I evaluated the system in five scenarios: `easy`, `standard`, `tight_budget`, `tight_time`, and `large_problem`. The main evaluation metrics were feasibility, number of visits, total satisfaction, travel ratio, daily balance, diversity, and runtime.
These scenarios were designed to test different kinds of pressure, including loose conditions, budget limits, time limits, and larger search spaces.

## Part 10. Results

The results show that beam search performs better than the greedy baseline in most scenarios. It ties greedy in the easy case and performs better in the standard, tight-budget, and large-problem settings. However, in the tight-time scenario, greedy performs better, which suggests that the current beam-search heuristic still gives too much weight to remaining budget when time is actually the main bottleneck.
This result is important because it shows both the strength and the limitation of heuristic search. Better search breadth helps in many cases, but a poorly matched heuristic can still reduce performance.

Another important result is that all generated itineraries are feasible, with zero validation violations across all experiments.
This gives additional confidence that the system is not only optimizing scores, but also consistently respecting the planning rules.

## Part 11. Conclusion

In conclusion, this project presents a complete prototype for constrained travel itinerary planning. It includes synthetic data generation, feasibility-aware planning, independent validation, and comparative experiments. The main takeaway is that beam search usually improves itinerary quality and balance, but heuristic design matters. In the future, this system could be improved with adaptive scoring, real map data, learned user preferences, and real-time replanning.
Overall, the project shows that constrained itinerary planning can be addressed effectively with practical AI methods, while still leaving clear opportunities for future improvement.
