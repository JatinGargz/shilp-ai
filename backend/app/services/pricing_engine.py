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

def evaluate_bargaining_offer(material_cost: float, labor_hours: float, offered_price: float, craft_type: str = "textiles") -> dict:
    SKILLED_HOURLY_WAGE = 100.0
    packaging = 50.0
    cost_floor = material_cost + (labor_hours * SKILLED_HOURLY_WAGE) + packaging
    
    effective_wage_pool = offered_price - material_cost - packaging
    effective_hourly_wage = max(0.0, effective_wage_pool / max(1.0, labor_hours))
    is_exploitative = effective_hourly_wage < SKILLED_HOURLY_WAGE
    
    # Fair counter-offer gives full wage floor + standard 15% minimum margin
    recommended_counter_offer = round(cost_floor * 1.18, -1)
    
    if is_exploitative:
        verdict = "EXPLOITATIVE_LOSS"
        status_hi = f"🛑 नुकसान का सौदा: आपकी दिहाड़ी गिरकर केवल ₹{effective_hourly_wage:.0f}/घंटा रह जाएगी (कानूनी ₹100 से कम)!"
        dialogue_hi = f"भैया, इसमें {labor_hours:.0f} घंटे की शुद्ध हाथ की मेहनत है। ₹{offered_price:.0f} में हमारी ₹50 की भी दिहाड़ी नहीं निकलती। सरकारी विश्वकर्मा योजना के तहत हमारा न्यूनतम नैतिक मूल्य ₹{recommended_counter_offer:.0f} है।"
        dialogue_en = f"Sir, this craft requires {labor_hours:.0f} hours of master craftsmanship. At ₹{offered_price:.0f}, the wage drops to ₹{effective_hourly_wage:.0f}/hr (below MoSJE skilled floor of ₹100/hr). The fair counter-offer is ₹{recommended_counter_offer:.0f}."
    else:
        verdict = "FAIR_PROFITABLE"
        status_hi = f"✓ उचित सौदा: इसमें आपको ₹{effective_hourly_wage:.0f}/घंटा की सुरक्षित मजदूरी मिल रही है।"
        dialogue_hi = f"जी धन्यवाद! यह सौदा उचित है। ₹{offered_price:.0f} में हम तुरंत काम शुरू कर सकते हैं।"
        dialogue_en = f"Offer accepted. Secures ethical wage of ₹{effective_hourly_wage:.0f}/hr."

    return {
        "offered_price": offered_price,
        "cost_floor": cost_floor,
        "effective_hourly_wage": round(effective_hourly_wage, 1),
        "is_exploitative": is_exploitative,
        "verdict": verdict,
        "recommended_counter_offer": recommended_counter_offer,
        "status_hi": status_hi,
        "dialogue_hi": dialogue_hi,
        "dialogue_en": dialogue_en
    }
