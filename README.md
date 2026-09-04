# 🇮🇳 SHILP AI (शिल्प) — Smart Handicraft Intelligence & Linkage Platform
### SIH 2026 Problem Statement ID: 26090 | Ministry of Social Justice and Empowerment (MoSJE)

> **A Voice-First AI Virtual Business Manager & Multi-Marketplace Publisher empowering marginalized artisans (PM Vishwakarma & PM-DAKSH) to photograph, catalog, price ethically, and distribute Indian handicrafts across 5 major e-commerce platforms.**

---

## ⭐ Key Highlights & Standout Features

1. **🎙️ Voice-First Native Dialect Cataloging:**
   - Artisans simply tap the mic and speak naturally in Hindi / regional dialects (*"Yeh pure Banarasi katan silk dupatta hai, haath se buna hua gold zari ke sath"*).
   - Generates bilingual, high-converting product descriptions (Hindi + English), material tags, and craft origin narratives with Groq Llama-3.3.
   - Synthesizes instant **Hindi Voice Feedback (TTS)** confirming catalog details and pricing aloud.

2. **📸 4K Studio Image Canvas + MoSJE Digital Seal:**
   - Automatically removes messy workshop backgrounds using `rembg` AI.
   - Centers and enhances crafts on a clean 1080×1080 e-commerce studio background.
   - Watermarks the official **MoSJE Digital Authenticity & GI Tag Seal** to prevent counterfeit knockoffs.

3. **⚖️ Anti-Exploitation Wage-Floor & "सौदा रक्षक" (Bargaining Shield):**
   - Ethical pricing engine calculating exact minimum living wages ($Material + (Hours \times ₹100/hr) + Packaging$) with craft category markups.
   - **Bargaining Shield Widget:** Evaluates buyer and tourist discount offers in real-time, flashing red on exploitative loss offers and suggesting polite, firm counter-offers.

4. **🚀 Universal 5-Marketplace Publisher (1-Click Distribution):**
   - **ONDC Network:** Generates compliant Beckn Protocol schema JSON for instant discoverability across buyer apps (Paytm, Pincode, Mystore).
   - **Amazon Karigar:** Generates Amazon-compliant ASIN feeds with 5 bullet points under the MoSJE Karigar MoU (5% subsidized fee).
   - **Flipkart Samarth:** Formats Flipkart FSN feeds with 0% introductory commission for handloom weavers.
   - **GeM (Govt e-Marketplace):** Formats tenders for The Saras Collection under GFR Rule 149 (4% mandated public procurement quota).
   - **Etsy Global Export:** Formats international listings in USD ($) for direct cross-border exports with DHL / India Post logistics.

5. **🤖 "शिल्प सखी" (Shilpi AI Voice Business Companion):**
   - Interactive voice advisor in Hindi providing guidance on PM Vishwakarma ₹15,000 toolkits, free exhibition stall bookings (Surajkund Mela), and e-commerce selling tips.

6. **📲 Instant WhatsApp Invoicing & Printable Mela Standees:**
   - Generates scannable dynamic UPI QR codes for zero-fee, middleman-free bank settlements.
   - Produces printable A4 Mela Standee PDFs with golden MoSJE certification borders.

---

## 👥 Team Roles & Responsibilities

| Role | Members | Core Ownership |
| :--- | :--- | :--- |
| **UI/UX & Design** | **Prakriti & Saira** | Figma design system, cultural color palette, dual-screen layout, and mobile simulator UX |
| **Frontend Technical** | **Jatin + Prakriti & Saira** | Multi-screen interactive simulator, multi-channel publisher drawer, audio synthesis, camera integration |
| **Backend & Database** | **Anikeat + Jatin** | FastAPI microservices, SQLite/SQLAlchemy schemas, multi-marketplace formatters, live order simulation |
| **AI / GenAI & Vision** | **Kartik Dhiman** | Background removal (`rembg`), Whisper STT, and Groq Llama-3.3 multilingual catalog engine |
| **ML & Pricing** | **Ishaan Anand** | Wage-floor ethical pricing algorithm, category markups, and Bargaining Shield engine |
| **DevOps & Integrations** | **Jatin** | ONDC Beckn schema, Amazon/Flipkart/GeM/Etsy feeds, automated test verification, and deployment |

---

## ⚡ Quick Start: Running the Prototype Locally

### 1. Start the Backend Server (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 2. Open the Multi-Channel Prototype (Browser)
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in Google Chrome or Microsoft Edge.

You will see the **Multi-Screen SIH Live Booth**:
- **📱 Left:** Artisan Mobile App Simulator (Voice mic, camera, 5-channel publish, Bargaining Shield, Shilpi voice companion).
- **🛒 Right:** Multi-Storefront & Ministry Central Portal:
  - View 1: **Paytm ONDC Network Buyer Storefront** (place order & watch instant sync to artisan phone!)
  - View 2: **Amazon Karigar Storefront** (ASIN listings with Prime & Karigar guarantee)
  - View 3: **MoSJE Central Ministry Portal** (Real-time artisan onboarding & cluster analytics)
  - View 4: **Split Demo Mode** (Side-by-side presentation mode for judges)

---

## 📁 Repository Structure

```
shilp-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes.py            # API route controllers
│   │   ├── models/models.py         # SQLAlchemy DB models (Artisan, Product, Pricing, Media)
│   │   ├── schemas/contracts.py     # Frozen data contracts
│   │   ├── services/
│   │   │   ├── image_studio.py      # rembg background removal + MoSJE watermark seal
│   │   │   ├── catalog_engine.py    # Groq Llama-3.3 auto-cataloger + gTTS Hindi audio
│   │   │   ├── pricing_engine.py    # Wage-floor pricing + Bargaining Shield
│   │   │   └── export_service.py    # Amazon, Flipkart, GeM, Etsy, ONDC & PDF generators
│   │   └── main.py                  # FastAPI orchestrator & static asset server
│   ├── test_kartik.py               # Kartik's vision & voice sandbox
│   ├── test_ishaan.py               # Ishaan's pricing & ML sandbox
│   └── requirements.txt             # Python dependencies
├── frontend/
│   └── index.html                   # Multi-Screen Web App (Mobile + Storefronts + Ministry Portal)
├── README.md                        # Project overview & quick start
└── TEAM_ONBOARDING_GUIDE.md         # Comprehensive team guide & beginner playbooks
```
