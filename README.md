FastBox Delivery System
A Python simulation of one day of delivery operations for a fictional logistics company, FastBox. The script assigns packages to the nearest delivery agent, simulates deliveries, and generates a performance report.

Approach Summary
I parsed the input JSON (handling two different data formats across test files), assigned each package to its nearest agent using Euclidean distance from agent to warehouse, then simulated deliveries by summing warehouse-to-destination distances per agent. Finally, I generated a report.json with each agent's packages delivered, total distance, and efficiency (distance ÷ packages), identifying the most efficient agent as best_agent. I tested the solution against all 10 provided test cases to confirm correctness.

How to Run
Make sure delivery_system.py and the JSON input file (e.g. base_case.json) are in the same folder, then run:

python delivery_system.py

Output format
{
  "A1": {"packages_delivered": 2, "total_distance": 64.14, "efficiency": 32.07},
  "A2": {"packages_delivered": 2, "total_distance": 36.18, "efficiency": 18.09},
  "A3": {"packages_delivered": 1, "total_distance": 7.07, "efficiency": 7.07},
  "best_agent": "A3"
}
Logic Assumptions
Tie-breaking: If two agents are equidistant from a warehouse, the first one found (iteration order) is picked.
Routing: Each delivery is treated as an independent warehouse→destination trip, not a continuous multi-stop route.
Efficiency formula: total_distance ÷ packages_delivered (derived from the sample numbers in the spec), lower = more efficient.
Best agent: Lowest efficiency, excluding agents with 0 deliveries (to avoid falsely favoring an idle agent).
Package order: Processed in input order, no extra prioritization.
Distance: Pure Euclidean distance, no path/obstacle logic, as required by the task.
Most Significant Technical Challenge

The biggest challenge was that the provided test files used inconsistent JSON formats — base_case.json structured warehouses/agents as a list of objects ([{"id": "W1", "location": [0,0]}]), while all 10 official test cases used a dictionary format instead ({"W1": [0,0]}), and package objects referenced their warehouse using two different key names (warehouse_id vs warehouse).

Resolution: I wrote a normalization function that detects the format using isinstance() and converts both shapes into one consistent internal structure before any distance calculations run. For packages, I used .get("warehouse", pkg.get("warehouse_id")) to handle either key. This let the same script run cleanly across all 10 test cases plus the base case, instead of crashing on 9 out of 10 files.

Files
delivery_system.py — main script
base_case.json — sample input from the assignment spec
test_case_1.json ... test_case_10.json — provided test inputs
report.json — generated output report
Bonus Features
