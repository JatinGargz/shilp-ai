def calculate_fair_pricing(material_cost: float, labor_hours: float, craft_type: str = "textiles") -> dict:
    SKILLED_HOURLY_WAGE = 100.0
    labor_wage = labor_hours * SKILLED_HOURLY_WAGE
    packaging = 50.0
    cost_floor = material_cost + labor_wage + packaging

    multipliers = {
        "textiles": 1.45,
        "pottery": 1.35,
        "metalwork": 1.50,
        "woodcraft": 1.40
    }
    multiplier = multipliers.get(craft_type.lower(), 1.40)
    
    retail = round(cost_floor * multiplier, -1)
    wholesale = round(cost_floor * 1.18, -1)

    return {
        "cost_floor": cost_floor,
        "recommended_retail_price": retail,
        "wholesale_b2b_price": wholesale,
        "guaranteed_labor_wage": labor_wage,
        "explanation": f"Guarantees Rs {labor_wage:.0f} skilled artisan wage ({labor_hours:.0f} hrs @ Rs 100/hr) + Rs {material_cost:.0f} raw materials + fair craft margin."
    }

def match_b2b_buyers(craft_type: str, price: float) -> list:
    all_buyers = [
        {"buyer_name": "Tribes India Regional Procurement Hub", "category": "metalwork", "demand_quantity": 50, "confidence_score": 96},
        {"buyer_name": "FabIndia Sustainable Sourcing Desk", "category": "textiles", "demand_quantity": 100, "confidence_score": 94},
        {"buyer_name": "Central Cottage Industries Emporium", "category": "pottery", "demand_quantity": 80, "confidence_score": 91},
        {"buyer_name": "Dastkar Craft Heritage Network", "category": "woodcraft", "demand_quantity": 40, "confidence_score": 93}
    ]
    matches = [b for b in all_buyers if b["category"] == craft_type.lower()]
    if not matches:
        matches = [all_buyers[0]]
    return matches
