"""
Budget calculation tools for GlobeTrotter AI.
"""

from typing import Any


def calculate_trip_budget(
    days: int,
    travel_style: str = "mid-range",
    num_travelers: int = 1,
    include_flights: bool = False,
) -> dict[str, Any]:
    """Calculates an estimated itemized trip budget breakdown for a destination itinerary.

    Args:
        days: Number of days for the trip (e.g. 3, 5, 7).
        travel_style: Travel comfort tier: 'budget', 'mid-range', or 'luxury'.
        num_travelers: Number of people traveling.
        include_flights: Whether to include estimated regional flights/transport.

    Returns:
        A dictionary containing itemized cost estimates for accommodation, food, activities, local transport, total cost, and daily cost per person in USD.
    """
    style = travel_style.lower().strip()

    rates = {
        "budget": {"lodging": 45, "food": 30, "activities": 20, "transport": 10},
        "mid-range": {"lodging": 120, "food": 65, "activities": 45, "transport": 25},
        "luxury": {"lodging": 350, "food": 160, "activities": 110, "transport": 60},
    }

    tier = rates.get(style, rates["mid-range"])

    lodging_total = tier["lodging"] * days * num_travelers
    food_total = tier["food"] * days * num_travelers
    activities_total = tier["activities"] * days * num_travelers
    local_transport_total = tier["transport"] * days * num_travelers

    flight_cost = (250 * num_travelers) if include_flights else 0

    subtotal = lodging_total + food_total + activities_total + local_transport_total + flight_cost
    contingency_buffer = round(subtotal * 0.10, 2)
    grand_total = round(subtotal + contingency_buffer, 2)

    return {
        "days": days,
        "travel_style": style,
        "num_travelers": num_travelers,
        "breakdown_usd": {
            "lodging": lodging_total,
            "food_and_dining": food_total,
            "activities_and_tours": activities_total,
            "local_transport": local_transport_total,
            "flights_or_transit": flight_cost,
            "contingency_buffer_10pct": contingency_buffer,
        },
        "total_budget_usd": grand_total,
        "cost_per_person_per_day_usd": round(grand_total / (days * max(num_travelers, 1)), 2),
    }
