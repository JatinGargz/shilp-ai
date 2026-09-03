def calculate_fair_pricing(material_cost: float, labor_hours: float, craft_type: str = "textiles"):
    """
    Calculates ethical pricing ensuring guaranteed artisan wages.
    """
    SKILLED_HOURLY_WAGE = 100.0  # Rs 100/hr skilled minimum wage
    labor_wage = labor_hours * SKILLED_HOURLY_WAGE
    cost_floor = material_cost + labor_wage
    
    multipliers = {
        "textiles": 1.45,
        "pottery": 1.35,
        "metalwork": 1.50,
        "woodcraft": 1.40
    }
    multiplier = multipliers.get(craft_type.lower(), 1.40)
    
    recommended_b2c = round(cost_floor * multiplier, -1)
    wholesale_b2b = round(cost_floor * 1.18, -1)
    
    return {
        "cost_floor": cost_floor,
        "recommended_retail_price": recommended_b2c,
        "wholesale_b2b_price": wholesale_b2b,
        "guaranteed_labor_wage": labor_wage,
        "explanation": f"Includes Rs {material_cost:.0f} raw materials + Rs {SKILLED_HOURLY_WAGE:.0f}/hr skilled wage guarantee ({labor_hours:.0f} hrs) + fair craft margin."
    }
