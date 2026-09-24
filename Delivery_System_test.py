import json
import math

def normalize_points(raw):
    """Convert either dict-style or list-style location data into
    a plain dict of {id: (x, y)}."""
    points = {}

    if isinstance(raw, dict):
        # Shape A: {"W1": [0, 0], ...}
        for point_id, coords in raw.items():
            points[point_id] = (coords[0], coords[1])

    elif isinstance(raw, list):
        # Shape B: [{"id": "W1", "location": [0, 0]}, ...]
        for entry in raw:
            points[entry["id"]] = (entry["location"][0], entry["location"][1])

    else:
        raise ValueError("Unrecognized format for warehouses/agents data")

    return points

def load_data(filepath):
    """Read the JSON file and return normalized warehouses, agents,
    and packages."""
    with open(filepath, "r") as f:
        data = json.load(f)

    warehouses = normalize_points(data["warehouses"])
    agents = normalize_points(data["agents"])

    packages = []
    for pkg in data["packages"]:
        warehouse_key = pkg.get("warehouse", pkg.get("warehouse_id"))
        packages.append({
            "id": pkg["id"],
            "warehouse": warehouse_key,
            "destination": tuple(pkg["destination"]),
        })

    return warehouses, agents, packages

# 2. DISTANCE CALCULATION

def euclidean_distance(point_a, point_b):
    """Straight-line distance between two (x, y) points."""
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)

# 3. ASSIGN EACH PACKAGE TO ITS NEAREST AGENT

def assign_packages(agents, warehouses, packages):
    """For every package, find the agent whose location is closest to
    the package's warehouse. Returns {agent_id: [package, package, ...]}."""
    assignments = {agent_id: [] for agent_id in agents}

    for pkg in packages:
        warehouse_loc = warehouses[pkg["warehouse"]]

        nearest_agent = None
        nearest_distance = float("inf")

        for agent_id, agent_loc in agents.items():
            dist = euclidean_distance(agent_loc, warehouse_loc)
            if dist < nearest_distance:
                nearest_distance = dist
                nearest_agent = agent_id

        assignments[nearest_agent].append(pkg)

    return assignments

# 4. SIMULATE DELIVERIES & BUILD THE REPORT

def simulate_and_report(assignments, warehouses):
    """For each agent, sum the warehouse->destination distance for every
    package they were assigned, then compute efficiency (avg distance
    per package). Lower efficiency = better (less distance per delivery)."""
    report = {}

    for agent_id, pkgs in assignments.items():
        total_distance = 0.0

        for pkg in pkgs:
            warehouse_loc = warehouses[pkg["warehouse"]]
            destination_loc = pkg["destination"]
            total_distance += euclidean_distance(warehouse_loc, destination_loc)

        delivered = len(pkgs)
        efficiency = round(total_distance / delivered, 2) if delivered else 0.0

        report[agent_id] = {
            "packages_delivered": delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": efficiency,
        }

    delivering_agents = {
        aid: r for aid, r in report.items() if r["packages_delivered"] > 0
    }
    if delivering_agents:
        best_agent = min(delivering_agents, key=lambda aid: delivering_agents[aid]["efficiency"])
    else:
        best_agent = None

    report["best_agent"] = best_agent
    return report

# 5. MAIN

def main(input_path="base_case.json", output_path="report.json"):
    warehouses, agents, packages = load_data(input_path)

    # Sanity check note from the assignment: total delivered must equal
    # total packages.
    assignments = assign_packages(agents, warehouses, packages)
    total_assigned = sum(len(pkgs) for pkgs in assignments.values())
    assert total_assigned == len(packages), "Mismatch: not all packages were assigned!"

    report = simulate_and_report(assignments, warehouses)

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report saved to {output_path}")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main("../base_case.json", "report.json")