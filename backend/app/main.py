from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import engine, Base, get_db
from app.core.seed import seed_database
from app.models.models import Artisan, Product
from app.schemas.contracts import ProcessRawResponse, CatalogData, PricingData, BuyerMatch
from app.services.catalog_engine import generate_catalog_from_voice
from app.services.pricing_engine import calculate_fair_pricing
from app.services.export_service import generate_upi_qr_bytes, generate_ondc_beckn_json, generate_mela_standee_pdf
import uuid

Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(title="SHILP AI Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "SHILP AI Core Orchestrator", "version": "1.0.0"}

@app.get("/api/v1/products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    results = []
    for p in products:
        results.append({
            "id": p.id,
            "title_en": p.title_en,
            "title_hi": p.title_hi,
            "craft_type": p.craft_type,
            "material": p.material,
            "artisan_name": p.artisan.name if p.artisan else "Master Artisan",
            "cluster": p.artisan.cluster if p.artisan else "Handicraft Cluster",
            "retail_price": p.pricing.recommended_retail_price if p.pricing else 500.0,
            "image_url": p.media.enhanced_studio_url if p.media else "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"
        })
    return {"count": len(results), "products": results}

@app.post("/api/v1/media/process-raw", response_model=ProcessRawResponse)
async def process_raw(
    craft_category: str = Form("textiles"),
    material_cost: float = Form(250.0),
    labor_hours: float = Form(16.0),
    artisan_name: str = Form("Master Artisan"),
    transcript_hint: str = Form("Banarasi Silk Dupatta handloom pure silk"),
    image_file: UploadFile = File(None),
    audio_file: UploadFile = File(None)
):
    prod_id = f"shilp_{uuid.uuid4().hex[:8]}"
    pricing_res = calculate_fair_pricing(material_cost, labor_hours, craft_category)
    catalog_res = generate_catalog_from_voice(transcript_hint, craft_category)
    
    return ProcessRawResponse(
        product_id=prod_id,
        status="READY_FOR_REVIEW",
        original_media_url="https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=800",
        enhanced_studio_url="https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800",
        detected_language="hi",
        raw_transcript=transcript_hint,
        catalog=CatalogData(
            title_en=catalog_res["title_en"],
            title_hi=catalog_res["title_hi"],
            craft_technique=catalog_res.get("craft_type", craft_category.title()),
            material=catalog_res.get("material", "Natural Craft Material"),
            story_en=catalog_res.get("story_en", "Authentic handcrafted piece by rural artisans."),
            bullet_points=catalog_res.get("bullet_points", ["Handmade", "Fair Wage Certified", "Heritage Art"]),
            audio_feedback_text_hi=catalog_res.get("audio_feedback_text_hi", f"Aapka {craft_category} safalta se catalog ho gaya hai.")
        ),
        pricing=PricingData(
            cost_floor=pricing_res["cost_floor"],
            recommended_retail_price=pricing_res["recommended_retail_price"],
            wholesale_b2b_price=pricing_res["wholesale_b2b_price"],
            guaranteed_labor_wage=pricing_res["guaranteed_labor_wage"],
            explanation=pricing_res["explanation"]
        ),
        buyer_matches=[
            BuyerMatch(buyer_name="Tribes India Procurement Desk", demand_quantity=100, confidence_score=96),
            BuyerMatch(buyer_name="FabIndia Sourcing Hub", demand_quantity=50, confidence_score=92)
        ]
    )

@app.get("/api/v1/products/{product_id}/upi-qr")
def get_upi_qr(product_id: str, amount: float = 590.0, artisan_name: str = "Shilp Artisan"):
    qr_bytes = generate_upi_qr_bytes(f"{product_id}@upi", artisan_name, amount)
    return Response(content=qr_bytes, media_type="image/png")

@app.get("/api/v1/products/{product_id}/mela-standee-pdf")
def get_mela_standee(product_id: str, title: str = "Handcrafted Artisan Diya", craft: str = "Brass Etching", price: float = 590.0):
    pdf_bytes = generate_mela_standee_pdf(product_id, title, craft, price, "Shilp Artisan")
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=mela_standee_{product_id}.pdf"}
    )

@app.get("/api/v1/products/{product_id}/export/ondc")
def get_ondc(product_id: str):
    mock_catalog = {"title_en": "Handcrafted Artisan Specialty", "story_en": "Preserving Indian heritage art."}
    mock_pricing = {"recommended_retail_price": 590.0}
    return generate_ondc_beckn_json(product_id, mock_catalog, mock_pricing, "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800")

@app.get("/api/v1/analytics/ministry")
def get_ministry_analytics():
    return {
        "total_artisans_onboarded": 1420,
        "total_catalogs_generated": 5840,
        "pm_vishwakarma_linked": 980,
        "total_estimated_sales_inr": 4250000.0,
        "active_clusters": [
            {"state": "Uttar Pradesh", "cluster": "Varanasi Silk", "count": 420},
            {"state": "Chhattisgarh", "cluster": "Bastar Dokra Metal", "count": 280},
            {"state": "Rajasthan", "cluster": "Jaipur Blue Pottery", "count": 350},
            {"state": "Gujarat", "cluster": "Kutch Rogan & Bandhani", "count": 370}
        ]
    }
