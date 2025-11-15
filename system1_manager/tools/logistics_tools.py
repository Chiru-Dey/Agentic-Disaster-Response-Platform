# system1_manager/tools/logistics_tools.py
from .schemas import (
    GetInventoryLevelsOutput,
    InventoryData,
    FindOptimalRouteOutput,
    RouteData
)

def get_inventory_levels(resource_type: str) -> GetInventoryLevelsOutput:
    """
    Checks the current inventory levels for a specified resource.

    Args:
        resource_type: The type of resource to check (e.g., 'water', 'food', 'medical_supplies').

    Returns:
        A structured output object with the status of the operation and the inventory data.
    """
    print(f"--- Tool: Checking inventory for {resource_type} ---")
    mock_inventory = {
        "water": {"units": 10000, "location": "main_warehouse"},
        "food": {"units": 5000, "location": "main_warehouse"},
        "medical_supplies": {"units": 1500, "location": "clinic_a"},
    }

    if resource_type in mock_inventory:
        inventory_data = InventoryData(**mock_inventory[resource_type])
        return GetInventoryLevelsOutput(status="success", data=inventory_data)
    else:
        return GetInventoryLevelsOutput(
            status="error",
            error_message=f"Resource type '{resource_type}' not found."
        )

def find_optimal_route(origin: str, destination: str, vehicle: str) -> FindOptimalRouteOutput:
    """
    Calculates the optimal route between an origin and a destination for a specific vehicle.

    Args:
        origin: The starting point of the route.
        destination: The destination point of the route.
        vehicle: The type of vehicle (e.g., 'truck', 'drone').

    Returns:
        A structured output object with the status and the calculated route data.
    """
    print(f"--- Tool: Calculating route from {origin} to {destination} for a {vehicle} ---")
    mock_route_data = {
        "distance_km": 125.0,
        "estimated_time_hours": 2.5,
        "waypoints": [origin, "waypoint_alpha", "waypoint_beta", destination]
    }
    route_data = RouteData(**mock_route_data)
    return FindOptimalRouteOutput(status="success", data=route_data)