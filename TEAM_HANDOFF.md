# 🇮🇳 SHILP AI (शिल्प) — Master Team Execution Plan
> **Problem Statement ID:** SIH26090  
> **Title:** AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans  
> **Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
> **Theme:** Heritage & Culture / Smart Automation / Rural Livelihoods  

---

## 📌 1. Project Vision & The Core Problem
India has over 20 million rural craftspeople, weavers, and tribal artisans supported by MoSJE financial assistance programs (NBCFDC, NSFDC, PM-DAKSH, PM Vishwakarma). While physical exhibitions (Shilp Samagam, Surajkund Mela, Dilli Haat) provide temporary sales bursts, artisans remain cut off from year-round digital commerce due to **low literacy, lack of photography skills, language barriers, and exploitation by middlemen**.

**Our Solution:** **SHILP AI** is an AI-powered *"Pocket Business Manager"* that empowers any artisan to snap a raw phone photo and speak a 10-second voice note in their regional language to instantly receive:
1. **A 4K Studio E-Commerce Photo** (automatic background removal and lighting correction).
2. **A Professional Bilingual Catalog** (SEO titles, bullet points, and heritage story in English + Hindi).
3. **An Audio Confirmation (TTS)** (the app speaks back in Hindi so illiterate artisans can verify details without reading).
4. **An Ethical Dynamic Price Recommendation** (guaranteed minimum wage floor + fair craft markup + B2B wholesale tier).
5. **1-Click Market Linkage** (Instant WhatsApp share card with UPI QR code + ONDC Beckn Protocol export JSON + Mela Standee QR PDF).

---

## 👥 2. Team Roster & Ownership Matrix

```
┌─────────────────────────┬────────────────────────────────────────────────────────┐
│ Team Member(s)          │ Role & Primary Ownership                               │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ 👤 Prakriti & Saira     │ Persons 1 & 2: UI/UX (Figma) + Frontend                │
│                         │ • Voice-first Mobile PWA (Artisan App)                 │
│                         │ • B2B Buyer & MoSJE Ministry Web Dashboard             │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ 👤 Anikeat              │ Person 3: Backend & Database Engine                    │
│                         │ • FastAPI REST server & orchestration                  │
│                         │ • Database schemas (PostgreSQL / SQLite) & migrations  │
│                         │ • Media storage endpoints & asynchronous job queues    │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ 👤 Kartik Dhiman        │ Person 4: AI / GenAI (Vision + Voice + Catalog)        │
│                         │ • AI Image Studio (`rembg` + OpenCV lighting)          │
│                         │ • Speech-to-Text (Whisper / Bhashini STT)              │
│                         │ • Guardrailed Multilingual Catalog Engine (LLM)        │
│                         │ • Voice-Back Audio Feedback (TTS) for low-literacy UX  │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ 👤 Ishaan Anand         │ Person 5: ML / Pricing & Market Data                   │
│                         │ • Hybrid Deterministic Cost-Floor & Pricing Algorithm  │
│                         │ • Wholesale B2B vs Retail B2C Tier Calculator          │
│                         │ • Explainable Pricing Reasons & B2B Buyer Matching     │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ 👤 Jatin                │ Integrations, DevOps & Pitch Lead                      │
│                         │ • Repository management & monorepo architecture        │
│                         │ • ONDC Beckn Schema & Mela Standee QR Generator        │
│                         │ • WhatsApp Card & UPI Payment Link Generator           │
│                         │ • Seed datasets & 5-minute SIH live pitch rehearsal    │
└─────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 🔒 3. Frozen API Contracts & Data Schemas

To ensure frontend and backend work simultaneously without blockers, all services will adhere strictly to these schemas:

### A. Media Upload & Processing Endpoint
* **Endpoint:** `POST /api/v1/media/process-raw`
* **Request (Multipart Form):**
  - `image_file`: Binary JPEG/PNG (raw product photo on floor/table)
  - `audio_file`: Binary WAV/MP3 (artisan spoken voice note)
  - `craft_category`: string (`textiles`, `pottery`, `metalwork`, `woodcraft`)
  - `material_cost`: float (raw material spent in ₹)
  - `labor_hours`: float (hours spent creating item)
* **Response (JSON):**
```json
{
  "product_id": "prod_a1b2c3d4",
  "status": "READY_FOR_REVIEW",
  "media": {
    "original_url": "https://storage.shilpai.in/raw/img_101.jpg",
    "enhanced_studio_url": "https://storage.shilpai.in/studio/img_101_studio.jpg"
  },
  "voice_transcription": {
    "detected_language": "hi",
    "raw_transcript": "Yeh pure pital ka hand-carved diya hai, do din lage banane me, 250 rupaye ka pital laga."
  },
  "catalog": {
    "title_en": "Handcrafted Pure Brass Traditional Diya with Etched Carvings",
    "title_hi": "पारंपरिक नक्काशीदार शुद्ध पीतल का हस्तनिर्मित दीया",
    "craft_type": "Moradabad Brass Etching",
    "material": "Pure Brass",
    "story_en": "Handcrafted by traditional brass artisans, keeping alive centuries of metallic artistry.",
    "bullet_points": [
      "100% Solid Brass with antique polish",
      "Hand-etched floral engravings by master artisans",
      "Direct procurement from artisan cluster"
    ],
    "audio_feedback_text_hi": "Aapka Pital ka Diya safalta se catalog ho gaya hai. Tajveez daam ₹590 hai.",
    "audio_feedback_url": "https://storage.shilpai.in/audio/feedback_101.mp3"
  },
  "pricing": {
    "cost_floor": 450.0,
    "recommended_retail_price": 590.0,
    "wholesale_b2b_price": 490.0,
    "guaranteed_labor_wage": 200.0,
    "explanation": "Includes ₹250 raw material + ₹100/hr skilled wage guarantee + 31% artisan craft markup."
  },
  "buyer_matches": [
    {
      "buyer_name": "Tribes India Regional Procurement",
      "demand_quantity": 100,
      "confidence_score": 96
    }
  ]
}
```

---

## 🚀 4. Detailed Role Instructions & Workflows

### For Prakriti & Saira (UI/UX & Frontend):
1. **Design System:** Use earthy, cultural, high-contrast Indian tones (Terracotta Orange `#D9531E`, Heritage Saffron `#E07A5F`, Deep Charcoal `#1D1E2C`, Pure Studio White `#FFFFFF`).
2. **Artisan Mobile App (PWA / Mobile Web):**
   - Keep interactions voice-first.
   - Screen 1: Big pulsing Mic Button + Camera Icon.
   - Screen 2: Before/After image comparison slider.
   - Screen 3: Audio review (app automatically plays `audio_feedback_url` so user hears confirmation).
   - Screen 4: Large 1-tap buttons: *"Share to WhatsApp"* and *"Download Mela QR"*.
3. **Ministry & B2B Web Dashboard:**
   - Visual India map with state clusters (Varanasi Handloom, Bastar Dokra, Jaipur Blue Pottery).
   - Live counters: Total Artisans Onboarded, Total Digital Catalogs Generated, PM Vishwakarma Beneficiaries.

### For Anikeat (Backend & Database):
1. Build the FastAPI core server with CORS enabled.
2. Implement SQLite/PostgreSQL models: `Artisan`, `Product`, `Media`, `Pricing`, `B2BMatch`.
3. Provide mock API responses immediately so Prakriti & Saira can test frontend screens.
4. Integrate Kartik's AI services and Ishaan's pricing module into the pipeline.

### For Kartik Dhiman (AI & GenAI Lead):
1. **Vision:** Use `rembg` (u2net/BiRefNet) to strip messy backgrounds, normalize lighting with OpenCV, and center product on a $1080\times 1080$ pure white canvas.
2. **Speech:** Transcribe audio using Whisper / Bhashini STT.
3. **LLM Catalog:** Use Groq Cloud Llama-3.3-70b with strict zero-hallucination guardrails (only extract stated materials; unknown fields must be `null`).
4. **Voice-Back:** Generate a short Hindi speech confirmation using gTTS or Bhashini TTS.

### For Ishaan Anand (ML & Pricing Lead):
1. Implement the deterministic cost floor formula:
   $$\text{Cost Floor} = \text{Material Cost} + (\text{Labor Hours} \times ₹100/\text{hr}) + \text{Packaging}$$
2. Implement the craft markup multiplier:
   - Handloom/Textiles: $1.45\times$
   - Terracotta/Pottery: $1.35\times$
   - Metalwork/Dokra: $1.50\times$
   - Woodcraft: $1.40\times$
3. Compute B2C Retail vs B2B Wholesale ($1.18\times$ floor).
4. Return an explainable sentence justifying the price.

### For Jatin (DevOps, Integrations & Pitch):
1. **ONDC Export:** Convert product record to ONDC Beckn schema JSON.
2. **Mela Standee:** Auto-generate a printable PDF stall standee with QR code using ReportLab.
3. **WhatsApp Card:** Generate dynamic UPI payment QR code (`upi://pay?pa=artisan@upi&am=...`).
4. **Demo Kit:** Procure 3 physical craft items and rehearse the 5-minute live booth pitch.

