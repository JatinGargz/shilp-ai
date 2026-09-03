from app.core.database import SessionLocal, engine, Base
from app.models.models import Artisan, Product, ProductMedia, ProductPricing

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(Artisan).count() > 0:
        db.close()
        return

    print("Seeding initial MoSJE artisan clusters and products...")
    clusters = [
        {"name": "Ramprasad Vishwakarma", "state": "Uttar Pradesh", "cluster": "Varanasi Silk Weavers", "craft": "textiles", "scheme": "PM-VISH-UP-0042"},
        {"name": "Mangli Bai Mandavi", "state": "Chhattisgarh", "cluster": "Bastar Dokra Metal Artisans", "craft": "metalwork", "scheme": "PM-DAKSH-CG-108"},
        {"name": "Govind Narain Kripalu", "state": "Rajasthan", "cluster": "Jaipur Blue Pottery", "craft": "pottery", "scheme": "NBCFDC-RJ-5521"},
        {"name": "Zubeda Begum", "state": "Gujarat", "cluster": "Kutch Rogan & Bandhani", "craft": "textiles", "scheme": "PM-VISH-GJ-8820"},
        {"name": "Subhash Chitrakar", "state": "Bihar", "cluster": "Madhubani Traditional Art", "craft": "woodcraft", "scheme": "NSFDC-BR-3091"}
    ]
    
    sample_products = [
        {
            "title_en": "Handwoven Banarasi Katan Silk Scarf with Gold Zari",
            "title_hi": "पारंपरिक बनारसी कतान सिल्क दुपट्टा (स्वर्ण ज़री)",
            "craft": "Banarasi Weaving",
            "material": "Pure Mulberry Silk",
            "story": "Woven by 5th-generation Varanasi handloom artisans preserving heritage motifs.",
            "bullets": "100% Handloom Silk|Gold Zari Border|Certified Craftmark",
            "orig_img": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=800",
            "studio_img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800",
            "cost_floor": 1200.0, "retail": 1850.0, "wholesale": 1450.0, "wage": 800.0,
            "explanation": "Guarantees 8 hours skilled artisan wage (Rs 800) + Rs 400 raw silk + 54% craft margin."
        },
        {
            "title_en": "Ancient Lost-Wax Cast Bastar Dokra Brass Diya",
            "title_hi": "प्राचीन लॉस्ट-वैक्स पद्धति से निर्मित बस्तर ढोकरा पीतल दीया",
            "craft": "Dokra Brass Casting",
            "material": "Recycled Brass & Bell Metal",
            "story": "Tribal artisans of Bastar crafting non-ferrous metal art using 4,000-year-old techniques.",
            "bullets": "Individually handcrafted|No two pieces identical|Traditional tribal motif",
            "orig_img": "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?w=800",
            "studio_img": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800",
            "cost_floor": 450.0, "retail": 690.0, "wholesale": 540.0, "wage": 300.0,
            "explanation": "Guarantees Rs 300 tribal artisan wage + Rs 150 metal alloy + 53% craft margin."
        },
        {
            "title_en": "Handmade Jaipur Blue Pottery Ceramic Floral Vase",
            "title_hi": "हस्तनिर्मित जयपुर ब्लू पॉटरी सिरेमिक फूलदान",
            "craft": "Blue Pottery",
            "material": "Quartz Stone & Multani Mitti",
            "story": "Low-fire dough glazed with traditional cobalt blue natural pigments.",
            "bullets": "Hand-painted floral arabesque|Eco-friendly clay glaze|Lead-free",
            "orig_img": "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=800",
            "studio_img": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=800",
            "cost_floor": 320.0, "retail": 490.0, "wholesale": 390.0, "wage": 200.0,
            "explanation": "Guarantees Rs 200 artisan wage + Rs 120 quartz/pigment + 53% craft margin."
        }
    ]
    
    for i, c in enumerate(clusters):
        artisan_id = f"artisan_{i+1:03d}"
        artisan = Artisan(
            id=artisan_id,
            name=c["name"],
            phone=f"+91 98765 {i+1:04d}",
            state=c["state"],
            cluster=c["cluster"],
            craft_type=c["craft"],
            scheme_id=c["scheme"]
        )
        db.add(artisan)
        
        if i < len(sample_products):
            sp = sample_products[i]
            prod_id = f"prod_{i+1:03d}"
            product = Product(
                id=prod_id,
                artisan_id=artisan_id,
                title_en=sp["title_en"],
                title_hi=sp["title_hi"],
                craft_type=sp["craft"],
                material=sp["material"],
                story_en=sp["story"],
                bullet_points=sp["bullets"],
                status="PUBLISHED"
            )
            db.add(product)
            
            media = ProductMedia(
                id=f"media_{i+1:03d}",
                product_id=prod_id,
                original_url=sp["orig_img"],
                enhanced_studio_url=sp["studio_img"]
            )
            db.add(media)
            
            pricing = ProductPricing(
                id=f"price_{i+1:03d}",
                product_id=prod_id,
                cost_floor=sp["cost_floor"],
                recommended_retail_price=sp["retail"],
                wholesale_b2b_price=sp["wholesale"],
                guaranteed_labor_wage=sp["wage"],
                explanation=sp["explanation"]
            )
            db.add(pricing)

    db.commit()
    print("Database seeded successfully with 5 artisans and 3 showcase products!")
    db.close()

if __name__ == "__main__":
    seed_database()
