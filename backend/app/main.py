import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
from sqlalchemy.orm import Session

from app.core.database import engine, Base, get_db
from app.core.seed import seed_database
from app.models.models import Artisan, Product, ProductMedia, ProductPricing
from app.schemas.contracts import ProcessRawResponse, CatalogData, PricingData, BuyerMatch
from app.services.image_studio import enhance_craft_image
from app.services.catalog_engine import generate_catalog_from_voice, generate_hindi_tts_audio, ask_shilpi_assistant
from app.services.pricing_engine import calculate_fair_pricing, match_b2b_buyers, evaluate_bargaining_offer
from app.services.export_service import generate_upi_qr_bytes, generate_ondc_beckn_json, generate_mela_standee_pdf, publish_to_all_channels


Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(title="SHILP AI Core Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
os.makedirs(os.path.join(STATIC_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "studio"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "audio"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_frontend_root():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "SHILP AI Core Orchestrator running"}

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
    artisan_name: str = Form("Ramprasad Vishwakarma"),
    transcript_hint: str = Form("Yeh pure Banarasi katan silk dupatta hai, haath se buna hua gold zari ke sath, do din lage banane me."),
    image_file: UploadFile = File(None),
    audio_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    prod_id = f"shilp_{uuid.uuid4().hex[:8]}"
    
    orig_url = "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=800"
    if image_file and image_file.filename:
        raw_bytes = await image_file.read()
        orig_filename = f"orig_{prod_id}.jpg"
        orig_path = os.path.join(STATIC_DIR, "uploads", orig_filename)
        with open(orig_path, "wb") as f:
            f.write(raw_bytes)
        orig_url = f"/static/uploads/{orig_filename}"
        enhanced_url = enhance_craft_image(raw_bytes, prod_id, STATIC_DIR)
    else:
        enhanced_url = enhance_craft_image(b"", prod_id, STATIC_DIR)
        
    catalog_res = generate_catalog_from_voice(transcript_hint, craft_category)
    pricing_res = calculate_fair_pricing(material_cost, labor_hours, craft_category)
    tts_url = generate_hindi_tts_audio(catalog_res["title_hi"], pricing_res["recommended_retail_price"], prod_id, STATIC_DIR)
    
    buyer_matches = match_b2b_buyers(craft_category, pricing_res["recommended_retail_price"])
    buyer_objs = [BuyerMatch(buyer_name=b["buyer_name"], demand_quantity=b["demand_quantity"], confidence_score=b["confidence_score"]) for b in buyer_matches]
    
    artisan = db.query(Artisan).first()
    artisan_id = artisan.id if artisan else "artisan_001"
    
    product = Product(
        id=prod_id,
        artisan_id=artisan_id,
        title_en=catalog_res["title_en"],
        title_hi=catalog_res["title_hi"],
        craft_type=catalog_res["craft_type"],
        material=catalog_res["material"],
        story_en=catalog_res["story_en"],
        bullet_points="|".join(catalog_res.get("bullet_points", [])),
        status="PUBLISHED"
    )
    db.add(product)
    
    media = ProductMedia(
        id=f"media_{prod_id}",
        product_id=prod_id,
        original_url=orig_url,
        enhanced_studio_url=enhanced_url
    )
    db.add(media)
    
    pricing = ProductPricing(
        id=f"price_{prod_id}",
        product_id=prod_id,
        cost_floor=pricing_res["cost_floor"],
        recommended_retail_price=pricing_res["recommended_retail_price"],
        wholesale_b2b_price=pricing_res["wholesale_b2b_price"],
        guaranteed_labor_wage=pricing_res["guaranteed_labor_wage"],
        explanation=pricing_res["explanation"]
    )
    db.add(pricing)
    db.commit()

    return ProcessRawResponse(
        product_id=prod_id,
        status="READY_FOR_REVIEW",
        original_media_url=orig_url,
        enhanced_studio_url=enhanced_url,
        detected_language="hi",
        raw_transcript=transcript_hint,
        catalog=CatalogData(
            title_en=catalog_res["title_en"],
            title_hi=catalog_res["title_hi"],
            craft_technique=catalog_res.get("craft_type", craft_category.title()),
            material=catalog_res.get("material", "Natural Craft Material"),
            story_en=catalog_res.get("story_en", "Authentic handcrafted piece by rural artisans."),
            bullet_points=catalog_res.get("bullet_points", ["Handmade", "Fair Wage Certified", "Heritage Art"]),
            audio_feedback_text_hi=f"Aapka {catalog_res['title_hi']} safalta se catalog ho gaya hai. Daam Rs {pricing_res['recommended_retail_price']:.0f} hai."
        ),
        pricing=PricingData(
            cost_floor=pricing_res["cost_floor"],
            recommended_retail_price=pricing_res["recommended_retail_price"],
            wholesale_b2b_price=pricing_res["wholesale_b2b_price"],
            guaranteed_labor_wage=pricing_res["guaranteed_labor_wage"],
            explanation=pricing_res["explanation"]
        ),
        buyer_matches=buyer_objs
    )

@app.get("/api/v1/products/{product_id}/upi-qr")
def get_upi_qr(product_id: str, amount: float = 590.0, artisan_name: str = "Shilp Artisan"):
    qr_bytes = generate_upi_qr_bytes(f"{product_id}@upi", artisan_name, amount)
    return Response(content=qr_bytes, media_type="image/png")

@app.get("/api/v1/products/{product_id}/mela-standee-pdf")
def get_mela_standee(product_id: str, title: str = "Handcrafted Artisan Specialty", craft: str = "Traditional Craft", price: float = 590.0):
    pdf_bytes = generate_mela_standee_pdf(product_id, title, craft, price, "Shilp Artisan")
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=mela_standee_{product_id}.pdf"}
    )

@app.get("/api/v1/products/{product_id}/export/ondc")
def get_ondc(product_id: str, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    title = prod.title_en if prod else "Handcrafted Traditional Item"
    price = prod.pricing.recommended_retail_price if prod and prod.pricing else 590.0
    img = prod.media.enhanced_studio_url if prod and prod.media else "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"
    return generate_ondc_beckn_json(product_id, {"title_en": title}, {"recommended_retail_price": price}, img)

@app.get("/export/ondc")
def get_global_ondc_export(db: Session = Depends(get_db)):
    prod = db.query(Product).first()
    pid = prod.id if prod else "prod_001"
    title = prod.title_en if prod else "Handcrafted Traditional Banarasi Scarf"
    price = prod.pricing.recommended_retail_price if prod and prod.pricing else 1850.0
    img = prod.media.enhanced_studio_url if prod and prod.media else "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"
    return generate_ondc_beckn_json(pid, {"title_en": title}, {"recommended_retail_price": price}, img)

@app.post("/api/v1/pricing/bargain-shield")
def post_bargaining_shield(payload: dict):
    material_cost = float(payload.get("material_cost", 350.0))
    labor_hours = float(payload.get("labor_hours", 16.0))
    offered_price = float(payload.get("offered_price", 1100.0))
    craft_type = payload.get("craft_type", "textiles")
    return evaluate_bargaining_offer(material_cost, labor_hours, offered_price, craft_type)

@app.post("/api/v1/assistant/shilpi")
def post_shilpi_assistant(payload: dict):
    question = payload.get("question", "")
    return ask_shilpi_assistant(question, STATIC_DIR)

@app.post("/api/v1/orders/simulate-ondc-order")
def simulate_ondc_order(payload: dict, db: Session = Depends(get_db)):
    prod_id = payload.get("product_id", "prod_001")
    buyer_name = payload.get("buyer_name", "Suman Rao")
    city = payload.get("city", "Mumbai, Maharashtra")
    qty = int(payload.get("quantity", 1))
    buyer_app = payload.get("buyer_app", "Paytm ONDC Store")
    
    prod = db.query(Product).filter(Product.id == prod_id).first()
    price = prod.pricing.recommended_retail_price if prod and prod.pricing else 2900.0
    total_amount = price * qty
    order_id = f"OD_ONDC_{uuid.uuid4().hex[:8].upper()}"
    
    return {
        "status": "ORDER_CONFIRMED",
        "order_id": order_id,
        "product_id": prod_id,
        "product_title": prod.title_en if prod else "Handcrafted Heritage Craft",
        "buyer_name": buyer_name,
        "delivery_city": city,
        "quantity": qty,
        "total_amount": total_amount,
        "buyer_network_app": buyer_app,
        "payment_status": "SETTLED_VIA_UPI",
        "artisan_credited": prod.artisan.name if prod and prod.artisan else "Ramprasad Vishwakarma",
        "artisan_upi_id": f"{prod_id}@upi",
        "timestamp": "Just now",
        "tracking_id": f"DELHIVERY_{uuid.uuid4().hex[:6].upper()}"
    }

@app.get("/api/v1/analytics/ministry")
def get_ministry_analytics(db: Session = Depends(get_db)):
    prod_count = db.query(Product).count()
    artisan_count = db.query(Artisan).count()
    return {
        "total_artisans_onboarded": 1420 + artisan_count,
        "total_catalogs_generated": 5840 + prod_count,
        "pm_vishwakarma_linked": 980,
        "total_estimated_sales_inr": 4250000.0,
        "active_clusters": [
            {"state": "Uttar Pradesh", "cluster": "Varanasi Silk", "count": 420},
            {"state": "Chhattisgarh", "cluster": "Bastar Dokra Metal", "count": 280},
            {"state": "Rajasthan", "cluster": "Jaipur Blue Pottery", "count": 350},
            {"state": "Gujarat", "cluster": "Kutch Rogan & Bandhani", "count": 370}
        ]
    }

@app.post("/api/v1/channels/publish-multi")
def post_multi_channel_publish(payload: dict, db: Session = Depends(get_db)):
    product_id = payload.get("product_id", "prod_001")
    prod = db.query(Product).filter(Product.id == product_id).first()
    
    catalog = {
        "title_en": prod.title_en if prod else "Handcrafted Traditional Banarasi Scarf",
        "craft_type": prod.craft_type if prod else "Banarasi Weaving",
        "material": prod.material if prod else "Pure Silk",
        "story_en": prod.story_en if prod else "500-year handloom heritage artifact."
    }
    pricing = {
        "recommended_retail_price": prod.pricing.recommended_retail_price if prod and prod.pricing else 2900.0,
        "wholesale_b2b_price": prod.pricing.wholesale_b2b_price if prod and prod.pricing else 2320.0
    }
    image_url = prod.media.enhanced_studio_url if prod and prod.media else "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"
    
    return publish_to_all_channels(product_id, catalog, pricing, image_url)

@app.get("/api/v1/products/{product_id}/channels")
def get_product_channels(product_id: str, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    catalog = {
        "title_en": prod.title_en if prod else "Handcrafted Traditional Artifact",
        "craft_type": prod.craft_type if prod else "Traditional Craft",
        "material": prod.material if prod else "Ethical Raw Material",
        "story_en": prod.story_en if prod else "Preserving Indian heritage."
    }
    pricing = {
        "recommended_retail_price": prod.pricing.recommended_retail_price if prod and prod.pricing else 2900.0,
        "wholesale_b2b_price": prod.pricing.wholesale_b2b_price if prod and prod.pricing else 2320.0
    }
    image_url = prod.media.enhanced_studio_url if prod and prod.media else "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"
    return publish_to_all_channels(product_id, catalog, pricing, image_url)



