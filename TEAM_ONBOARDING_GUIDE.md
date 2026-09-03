# 🇮🇳 SHILP AI — Team Onboarding & Kickoff Guide
> **SIH 2026 Problem Statement ID:** 26090  
> **Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
> **Project Repository:** `shilp-ai`  

---

## 👋 Welcome Team!
We are building **SHILP AI (शिल्प)** — an AI-powered platform empowering rural, marginalized, and PM Vishwakarma artisans to catalog their crafts, generate studio-grade photography, calculate fair prices, and sell directly via ONDC and WhatsApp using only their **voice and phone camera**.

To ensure everyone can work fast and independently **without blocking each other or causing Git merge conflicts**, follow this guide carefully.

---

## 🛡️ The Golden Rule: Zero-Conflict File Ownership
Each person/sub-team has their **own dedicated files and folders**. **Do NOT edit files assigned to another teammate.**

```
shilp-ai/
│
├── 🎨 FRONTEND WORKSPACE ──────────> Prakriti & Saira
│   ├── frontend-mobile/             (Voice-first mobile artisan app)
│   └── frontend-admin/              (Ministry analytics & B2B dashboard)
│
├── ⚙️ BACKEND & DATABASE WORKSPACE ──> Anikeat
│   ├── backend/app/models/          (SQLAlchemy database tables)
│   └── backend/app/api/             (CRUD endpoints & file upload handlers)
│
├── 🧠 AI & GEN-AI WORKSPACE ────────> Kartik Dhiman
│   ├── backend/app/services/image_studio.py   (rembg + OpenCV 1080x1080 canvas)
│   └── backend/app/services/catalog_engine.py (Whisper STT + Groq Llama-3 catalog)
│
├── 📊 ML & PRICING WORKSPACE ────────> Ishaan Anand
│   └── backend/app/services/pricing_engine.py (Ethical pricing + B2B buyer matcher)
│
└── 🎖️ INTEGRATIONS & DEMO ───────────> Jatin
    ├── backend/app/services/export_service.py (ONDC Beckn JSON + Mela Standee PDF + UPI QR)
    ├── backend/app/schemas/contracts.py       (FROZEN CONTRACT - Do not change)
    └── demo-assets/                           (Physical demo samples & recordings)
```

---

## ⚡ 5-Minute Local Setup (For All Developers)

### 1. Clone & Set Up Git
```bash
git clone <repo-url>
cd shilp-ai
```

### 2. Set Up Your Dedicated Branch
Always work on your own branch. Never commit directly to `main`:
* **Prakriti & Saira:** `git checkout -b frontend/artisan-mobile` or `frontend/ministry-admin`
* **Anikeat:** `git checkout -b backend/database-apis`
* **Kartik Dhiman:** `git checkout -b ai/vision-voice-pipeline`
* **Ishaan Anand:** `git checkout -b ml/pricing-engine`

### 3. Start the Backend Server (With Live Mocks)
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows (or source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
> **Notice:** The backend is **already running with mock data** matching our frozen API contract! Frontend developers can start building screens immediately without waiting for AI models to be finished.

---

## 👤 Step-by-Step Playbooks for Each Teammate

---

### 🎨 1. Prakriti & Saira (UI/UX & Frontend)
* **Assigned Folders:** `frontend-mobile/` and `frontend-admin/`
* **Your Mission:** Build a voice-first interface so simple that a low-literacy artisan can catalog a craft in 3 taps, plus an executive analytics dashboard for MoSJE officers.

#### Step-by-Step Action Plan:
1. **Figma Wireframes (Hours 0–4):**
   * **Mobile App (Artisan):**
     * *Screen 1 (Home):* Prominent microphone button (*"Tap to Speak"*), camera button, and language toggle (Hindi / English / Marathi).
     * *Screen 2 (Studio Review):* Split slider showing raw uploaded photo vs. clean white studio output.
     * *Screen 3 (Catalog & Voice-Back):* Bilingual title, heritage story, fair price tag, and an audio player that speaks back the summary.
     * *Screen 4 (Success):* 1-Click *"Share on WhatsApp"* and *"Download Mela QR Standee"* buttons.
   * **Admin Dashboard (Ministry):**
     * Central map/cards showing total artisans onboarded, catalogs created, and PM Vishwakarma linked beneficiaries.
2. **Frontend Coding (Hours 4–18):**
   * Build the UI in your preferred framework (React / Next.js / Flutter / React Native) inside `frontend-mobile/` and `frontend-admin/`.
3. **Connect to the Live Mock Backend:**
   * Make a `POST` request to `http://localhost:8000/api/v1/media/process-raw`
   * You will receive real mock data matching [`backend/app/schemas/contracts.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/schemas/contracts.py).

---

### ⚙️ 2. Anikeat (Backend & Database)
* **Assigned Files:** `backend/app/models/models.py`, `backend/app/api/`, `backend/app/core/database.py`
* **Your Mission:** Build the database engine and API endpoints connecting the frontend to Kartik's AI and Ishaan's pricing algorithms.

#### Step-by-Step Action Plan:
1. **Database Models (`backend/app/models/models.py`):**
   * Refine and test the SQLAlchemy models: `Artisan`, `Product`, `ProductMedia`, `ProductPricing`, and `B2BEnquiry`.
   * Ensure relationships between `Product` and `Artisan` are working smoothly with SQLite / PostgreSQL.
2. **API Routes (`backend/app/api/`):**
   * `POST /api/v1/media/upload`: Store uploaded camera photos and audio files to disk or cloud storage.
   * `GET /api/v1/products`: Return all cataloged products for the marketplace grid.
   * `GET /api/v1/products/{id}`: Return single product details.
   * `POST /api/v1/products/{id}/enquiry`: Save B2B wholesale enquiries.
3. **Pipeline Orchestration:**
   * In `backend/app/main.py`, connect the uploaded files to Kartik's `enhance_craft_image()` and `generate_catalog_from_voice()`, and Ishaan's `calculate_fair_pricing()`.

---

### 🧠 3. Kartik Dhiman (AI / GenAI & Vision)
* **Assigned Files:** 
  * [`backend/app/services/image_studio.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/image_studio.py)
  * [`backend/app/services/catalog_engine.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/catalog_engine.py)
* **Your Mission:** Convert messy phone photos into 4K e-commerce studio shots, and translate spoken dialect voice notes into bilingual, structured catalog listings.

#### Step-by-Step Action Plan:
1. **Image Studio Pipeline (`image_studio.py`):**
   * Use `rembg` (u2net / BiRefNet) to strip messy table/floor backgrounds from incoming photos.
   * Use OpenCV/PIL to boost natural craft color saturation (+15%).
   * Create a $1080 \times 1080$ pure white canvas and center the product.
2. **Speech-to-Text (`catalog_engine.py`):**
   * Implement `transcribe_audio_voice()` using OpenAI Whisper or Bhashini STT API to transcribe Hindi/Hinglish audio notes into text.
3. **Guardrailed Catalog Generator (`catalog_engine.py`):**
   * Call Groq Cloud API using `llama-3.3-70b-versatile` with JSON mode enabled.
   * Enforce strict zero-hallucination rules (only extract stated facts; unknown dimensions must be `null`).
   * Generate an English title, Hindi title, 2-line emotional artisan heritage story, and bullet points.
4. **Voice-Back (TTS):**
   * Generate a short Hindi audio confirmation using `gTTS` so illiterate artisans can verify their listing by listening.

---

### 📊 4. Ishaan Anand (ML / Pricing & Market Linkage)
* **Assigned File:** [`backend/app/services/pricing_engine.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/pricing_engine.py)
* **Your Mission:** Build an explainable, data-backed dynamic pricing model and B2B buyer recommendation engine so artisans are never cheated by middlemen.

#### Step-by-Step Action Plan:
1. **Cost Floor & Wage Guarantee Formula:**
   * Calculate:
     $$\text{Cost Floor} = \text{Raw Material Cost} + (\text{Labor Hours} \times ₹100/\text{hr Skilled Wage}) + \text{Packaging}$$
2. **Category Multipliers:**
   * Apply craft-specific fair markups:
     * Textiles / Handloom: $1.45\times$
     * Pottery / Ceramics: $1.35\times$
     * Metalwork / Dokra: $1.50\times$
     * Woodcraft: $1.40\times$
3. **Two-Tier Pricing:**
   * Calculate **Retail Price (B2C)** and **Wholesale Price (B2B)** ($1.18\times$ floor for bulk orders $\ge 25$ units).
4. **Explainable Pricing Sentence:**
   * Generate a human-readable justification (e.g., *"Guarantees ₹100/hr skilled wage for 16 hours + ₹350 raw silk + 45% fair craft markup."*).
5. **B2B Buyer Matching:**
   * Implement `match_b2b_buyers()` to match craft categories with institutional buyers (Tribes India, FabIndia, Central Cottage Industries Emporium).

---

### 🎖️ 5. Jatin (DevOps, Integrations & Pitch Lead)
* **Assigned Files:** [`backend/app/services/export_service.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/export_service.py), `demo-assets/`
* **Mission:** External commerce linkages, booth demo kit, and team orchestration.

#### Step-by-Step Action Plan:
1. **External Exports (`export_service.py`):**
   * Maintain the ONDC Beckn Protocol JSON schema.
   * Generate dynamic UPI payment QR codes (`upi://pay?pa=...`).
   * Generate printable A4 Mela Standee PDFs using ReportLab.
2. **Demo Kit & Seed Data:**
   * Maintain sample physical crafts and offline fallback recordings in `demo-assets/`.
3. **Repository & Merge Management:**
   * Review Pull Requests and merge into `main` after smoke tests pass.
4. **SIH 5-Minute Pitch:**
   * Direct and rehearse the live physical booth presentation with the team.

---

## 🔄 The Team Synchronization Workflow

```
[ Prakriti & Saira ]  ──> Building UI against Mock API (100% Unblocked)
[ Kartik Dhiman    ]  ──> Developing Vision & Voice in `image_studio.py` & `catalog_engine.py`
[ Ishaan Anand     ]  ──> Developing Pricing Math in `pricing_engine.py`
[ Anikeat          ]  ──> Developing Database & API routing in `models/` & `api/`
[ Jatin            ]  ──> Managing ONDC export, repo health & pitch assets
```

### When Ready to Merge:
1. Ensure your module runs without errors.
2. Push your branch:
   ```bash
   git push origin <your-branch-name>
   ```
3. Open a Pull Request into `main`.
4. Jatin will verify with `python -m backend.tests.test_api` and merge!

Let's build a winning SIH prototype! 🇮🇳
