# system1_manager/tools/schemas.py
from pydantic import BaseModel, Field
from typing import List, Literal

# --- Base Tool Output Schema ---

class ToolOutput(BaseModel):
    """Base model for all tool outputs."""
    status: Literal["success", "error"]
    error_message: str | None = None

# --- Inventory Tool Schemas ---

class InventoryData(BaseModel):
    """Structured data for inventory levels."""
    units: int = Field(..., description="The number of units available.")
    location: str = Field(..., description="The location of the inventory.")

class GetInventoryLevelsOutput(ToolOutput):
    """Output schema for the get_inventory_levels tool."""
    data: InventoryData | None = None

# --- Routing Tool Schemas ---

class RouteData(BaseModel):
    """Structured data for a calculated route."""
    distance_km: float = Field(..., description="The total distance of the route in kilometers.")
    estimated_time_hours: float = Field(..., description="The estimated travel time in hours.")
    waypoints: List[str] = Field(..., description="A list of waypoints from origin to destination.")

class FindOptimalRouteOutput(ToolOutput):
    """Output schema for the find_optimal_route tool."""
    data: RouteData | None = None