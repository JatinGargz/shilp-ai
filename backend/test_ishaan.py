import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services.pricing_engine import calculate_fair_pricing, match_b2b_buyers

print("=" * 60)
print("  ISHAAN\'S PRICING & MARKET DATA SANDBOX TEST")
print("=" * 60)

print("\n[Testing Fair Pricing Algorithm...]")
pricing_result = calculate_fair_pricing(material_cost=350.0, labor_hours=16.0, craft_type="textiles")

print("Cost Floor:               Rs.", pricing_result.get("cost_floor"))
print("Guaranteed Labor Wage:    Rs.", pricing_result.get("guaranteed_labor_wage"))
print("Recommended Retail (B2C): Rs.", pricing_result.get("recommended_retail_price"))
print("Wholesale Bulk (B2B):     Rs.", pricing_result.get("wholesale_b2b_price"))
print("Pricing Justification:   ", pricing_result.get("explanation"))

print("\n[Testing B2B Buyer Recommendation...]")
buyers = match_b2b_buyers(craft_type="textiles", price=pricing_result.get("recommended_retail_price", 1000.0))
for b in buyers:
    print(f"-> Matched: {b['buyer_name']} | Demand: {b['demand_quantity']} units | Match: {b['confidence_score']}%")

print("\n[SUCCESS] Ishaan\'s test ran cleanly! Now edit backend/app/services/pricing_engine.py to refine your formulas.")
