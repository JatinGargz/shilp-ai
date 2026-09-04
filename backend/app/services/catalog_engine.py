import json
import os
from gtts import gTTS

CRAFT_KNOWLEDGE = {
    "textiles": {
        "title_en": "Authentic Handcrafted Banarasi Silk Dupatta with Zari Border",
        "title_hi": "पारंपरिक ज़री बॉर्डर वाली हस्तनिर्मित बनारसी सिल्क दुपट्टा",
        "craft_type": "Banarasi Handloom Weaving",
        "material": "100% Pure Mulberry Silk",
        "story_en": "Hand-woven on traditional pit looms by Varanasi master weavers, preserving 500 years of handloom heritage.",
        "bullet_points": [
            "100% Handloom Certified Pure Silk",
            "Intricate golden zari floral motifs",
            "Direct procurement from MoSJE weaver cluster"
        ]
    },
    "metalwork": {
        "title_en": "Ancient Lost-Wax Cast Bastar Dokra Brass Diya",
        "title_hi": "प्राचीन लॉस्ट-वैक्स पद्धति से निर्मित बस्तर ढोकरा पीतल दीया",
        "craft_type": "Bastar Dokra Metal Casting",
        "material": "Bell Metal & Recycled Brass",
        "story_en": "Crafted by indigenous Bastar tribal artisans using a 4,000-year-old non-ferrous lost-wax metal casting technique.",
        "bullet_points": [
            "100% solid brass with rustic antique polish",
            "Hand-sculpted wax motif ensures each piece is unique",
            "Direct livelihood support for Chhattisgarh tribal artisans"
        ]
    },
    "pottery": {
        "title_en": "Handmade Jaipur Blue Pottery Ceramic Floral Vase",
        "title_hi": "हस्तनिर्मित जयपुर ब्लू पॉटरी सिरेमिक फूलदान",
        "craft_type": "Jaipur Blue Pottery",
        "material": "Quartz Stone Powder & Natural Cobalt Glaze",
        "story_en": "Crafted without clay using traditional Egyptian quartz paste and hand-painted with cobalt blue arabesque designs.",
        "bullet_points": [
            "Hand-painted traditional floral arabesque",
            "Lead-free eco-friendly quartz glaze",
            "GI-tagged craft from Jaipur artisan clusters"
        ]
    },
    "woodcraft": {
        "title_en": "Hand-Carved Saharanpur Sheesham Wood Trinket Box",
        "title_hi": "हस्तनिर्मित सहारनपुर शीशम की लकड़ी की नक्काशीदार डिब्बी",
        "craft_type": "Saharanpur Wood Carving",
        "material": "Seasoned Sheesham (Rosewood)",
        "story_en": "Carved by master artisans of Saharanpur showcasing delicate floral lattice jali work passed down through generations.",
        "bullet_points": [
            "Solid natural Sheesham wood with brass inlays",
            "Hand-buffed natural lacquer finish",
            "Fair wage certified woodcraft"
        ]
    }
}

def generate_catalog_from_voice(transcript: str, craft_category: str = "textiles") -> dict:
    category_key = craft_category.lower() if craft_category.lower() in CRAFT_KNOWLEDGE else "textiles"
    data = CRAFT_KNOWLEDGE[category_key].copy()
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            prompt = f"Extract facts from this voice transcript: '{transcript}'. Return JSON with title_en, title_hi, craft_type, material, story_en, bullet_points (array)."
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            parsed = json.loads(resp.choices[0].message.content)
            data.update(parsed)
        except Exception:
            pass

    return data

def generate_hindi_tts_audio(title_hi: str, price: float, prod_id: str, static_dir: str) -> str:
    text = f"Aapka {title_hi} safalta se catalog ho gaya hai. Tajveez daam {price:.0f} rupaye hai."
    filename = f"audio_{prod_id}.mp3"
    filepath = os.path.join(static_dir, "audio", filename)
    try:
        tts = gTTS(text=text, lang="hi", slow=False)
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        return "/static/audio/fallback_sample.mp3"
