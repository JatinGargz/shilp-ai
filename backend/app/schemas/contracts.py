from pydantic import BaseModel, Field
from typing import List, Optional

class CatalogData(BaseModel):
    title_en: str = Field(description="Professional English e-commerce title")
    title_hi: str = Field(description="Professional Hindi title")
    craft_technique: str = Field(description="Identified craft/handloom technique")
    material: Optional[str] = Field(default=None, description="Primary raw material used")
    story_en: str = Field(description="2-line emotional artisan heritage story")
    bullet_points: List[str] = Field(description="Key product features")
    audio_feedback_text_hi: str = Field(description="Short Hindi confirmation text for TTS")

class PricingData(BaseModel):
    cost_floor: float = Field(description="Minimum production cost floor in INR")
    recommended_retail_price: float = Field(description="Recommended B2C price in INR")
    wholesale_b2b_price: float = Field(description="Recommended B2B bulk price in INR")
    guaranteed_labor_wage: float = Field(description="Guaranteed artisan labor wage earned")
    explanation: str = Field(description="Justification for calculated price")

class BuyerMatch(BaseModel):
    buyer_name: str
    demand_quantity: int
    confidence_score: int

class ProcessRawResponse(BaseModel):
    product_id: str
    status: str
    original_media_url: str
    enhanced_studio_url: str
    detected_language: str
    raw_transcript: str
    catalog: CatalogData
    pricing: PricingData
    buyer_matches: List[BuyerMatch]
