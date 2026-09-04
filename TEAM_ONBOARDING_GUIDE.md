# 🇮🇳 SHILP AI — Complete Beginner's Team Onboarding Guide
> **SIH 2026 Problem Statement ID:** 26090  
> **Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
> **Project Repository:** `shilp-ai`  

---

## 🎯 Important Update: Our Winning Frontend Strategy
To save 15+ hours of Android SDK / Gradle troubleshooting and ensure our live demo never crashes in front of the judges, **we are using a Unified Web App with an Artisan Mobile Frame Simulator (PWA)** instead of a native APK.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DUAL-SCREEN HACKATHON BOOTH VIEW                                │
│                                                                                        │
│   📱 LEFT SIDE: Artisan Mobile Simulator (PWA) │  💻 RIGHT SIDE: Ministry Dashboard    │
│   • Runs inside a realistic phone mockup frame │  • Live counters for MoSJE officers   │
│   • Tap Mic -> Speak Hindi -> Take Photo       │  • State cluster registry table       │
│   • 4K Studio Image + WhatsApp Card + UPI QR   │  • Counters update in real time!      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
> **How to pitch this to SIH Judges:**  
> *"We architected this as an ultra-lightweight Progressive Web App (<2MB) because rural artisans use budget Android phones with low storage where heavy 60MB Play Store apps fail to install. With a PWA, any artisan can tap a WhatsApp link and start cataloging immediately with zero installation barrier."*

---

## 🛡️ Team Roles & Collaborative Ownership Map

| Domain | Teammates | Core Focus |
| :--- | :--- | :--- |
| **UI/UX & Product Design** | **Prakriti & Saira** | Figma wireframes, UI design tokens, color palette, visual assets, and UX flow |
| **Frontend Technical** | **Jatin + Prakriti & Saira** | Web code implementation, JavaScript state, API fetch integration, and mobile simulator |
| **Backend & Database** | **Anikeat + Jatin** | FastAPI server, database models & migrations, CRUD endpoints, and AI pipeline orchestration |
| **AI / GenAI & Vision** | **Kartik Dhiman** | Background removal (`rembg`), OpenCV canvas centering, Whisper STT, and Groq Llama-3 catalog |
| **ML & Pricing** | **Ishaan Anand** | Dynamic wage-floor pricing algorithm, craft markups, and B2B buyer recommendation |
| **DevOps & Integrations** | **Jatin** | ONDC Beckn schema, dynamic UPI QR generator, printable Mela Standee PDF, and SIH pitch |

```
shilp-ai/
│
├── 🎨 FRONTEND WORKSPACE ──────────> Prakriti & Saira (Design) + Jatin (Tech)
│   └── frontend/index.html          (Unified Web App: Mobile Simulator + Ministry Dashboard)
│
├── ⚙️ BACKEND & DATABASE WORKSPACE ──> Anikeat (Models & CRUD) + Jatin (Orchestration)
│   ├── backend/app/models/          (Database tables & SQLAlchemy models)
│   └── backend/app/api/             (CRUD routes & file upload endpoints)
│
├── 🧠 AI & GEN-AI WORKSPACE ────────> Kartik Dhiman
│   ├── backend/app/services/image_studio.py   (rembg + OpenCV 1080x1080 canvas)
│   ├── backend/app/services/catalog_engine.py (Whisper STT + Groq Llama-3 catalog)
│   └── backend/test_kartik.py                 (Kartik's 1-click test sandbox)
│
├── 📊 ML & PRICING WORKSPACE ────────> Ishaan Anand
│   ├── backend/app/services/pricing_engine.py (Ethical wage floor + B2B buyer matcher)
│   └── backend/test_ishaan.py                 (Ishaan's 1-click test sandbox)
│
└── 🎖️ INTEGRATIONS & DEMO ───────────> Jatin
    ├── backend/app/services/export_service.py (ONDC Beckn JSON + Mela Standee PDF + UPI QR)
    ├── backend/app/schemas/contracts.py       (FROZEN CONTRACT - Do not change)
    └── demo-assets/                           (Physical craft items & test samples)
```

---

## 🛠️ Step 0: Absolute Beginner Setup (For All Teammates)

1. **Install Required Software:**
   * Download and install **[VS Code](https://code.visualstudio.com/)**.
   * Download and install **[Python 3.10+](https://www.python.org/downloads/)** (Check the box that says *"Add python.exe to PATH"* during installation!).
   * Download and install **[Git](https://git-scm.com/)**.
2. **Open the Project:**
   * Open VS Code $ightarrow$ `File` $ightarrow$ `Open Folder...` $ightarrow$ Select the `shilp-ai` folder.
3. **Open Terminal in VS Code:**
   * Press `Ctrl + ~` (or go to menu: `Terminal` $ightarrow$ `New Terminal`).
4. **Create Your Personal Branch:**
   * Run the command matching your assigned area:
     ```bash
     # Frontend (Prakriti, Saira, Jatin):
     git checkout -b frontend/dual-view-suite

     # Backend (Anikeat, Jatin):
     git checkout -b backend/database-apis

     # AI / GenAI (Kartik Dhiman):
     git checkout -b ai/vision-voice-pipeline

     # ML & Pricing (Ishaan Anand):
     git checkout -b ml/pricing-engine
     ```

---

## 👤 Beginner Playbooks by Team Area

---

### 🎨 1. Frontend: Prakriti & Saira (Design) + Jatin (Tech)
> **Goal:** Create an ultra-intuitive visual experience for rural artisans and a professional central dashboard for MoSJE officers.

#### How We Collaborate:
* **Prakriti & Saira (Design Leads):**
  1. Open Figma and create the wireframes:
     * **Mobile View:** Minimalist, voice-first, large touch targets, cultural Indian color palette (Terracotta Orange `#D9531E`, Heritage Saffron `#E07A5F`, Deep Charcoal `#1F2937`).
     * **Ministry Dashboard:** Clean executive analytics cards and state cluster tables.
  2. Double-click [`frontend/index.html`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/frontend/index.html) in Chrome to view the working prototype.
  3. Work on visual assets, color codes, layouts, and button icons.
* **Jatin (Technical Lead on Frontend):**
  1. Handles the JavaScript wiring, state transitions, and camera/microphone event listeners.
  2. Connects the UI to `POST http://localhost:8000/api/v1/media/process-raw`.
  3. Implements the dynamic counter updates on the Ministry dashboard when a product is cataloged.

---

### ⚙️ 2. Backend: Anikeat (Models & Database) + Jatin (Orchestration & APIs)
> **Goal:** Run the FastAPI backend server, maintain database persistence, and orchestrate the AI/ML pipelines.

#### How We Collaborate:
* **Anikeat (Database & CRUD Lead):**
  1. Starts the server: `cd backend && python -m uvicorn app.main:app --reload --port 8000`.
  2. Opens **[http://localhost:8000/docs](http://localhost:8000/docs)** to test endpoints in Swagger UI.
  3. Expands [`backend/app/models/models.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/models/models.py) with database columns for artisan profiles and schemes.
  4. Implements local image storage in `backend/app/api/` for uploaded photos.
* **Jatin (Backend Architecture & Orchestration):**
  1. Wires Kartik's `image_studio.py` and `catalog_engine.py` into the main `/process-raw` route.
  2. Wires Ishaan's `pricing_engine.py` into the product creation pipeline.
  3. Ensures API responses match the frozen schema in [`contracts.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/schemas/contracts.py).

---

### 🧠 3. For Kartik Dhiman (AI / GenAI & Vision)
> **Goal:** Convert phone photos into studio-grade e-commerce images and translate voice notes into bilingual listings. You do NOT need to touch the web server to develop your code!

#### How to Start (Step-by-Step):
1. **Run Your 1-Click Sandbox Test:**
   * Open terminal and run:
     ```bash
     cd backend
     python test_kartik.py
     ```
   * It will test your functions and print the outputs immediately.
2. **Task A — Build Image Studio (`backend/app/services/image_studio.py`):**
   * Use `rembg` to remove cluttered backgrounds.
   * Boost color saturation (+15%) using PIL/OpenCV.
   * Center the product onto a clean $1080 	imes 1080$ pure white canvas.
3. **Task B — Voice to Catalog (`backend/app/services/catalog_engine.py`):**
   * Use Groq Cloud API (`llama-3.3-70b-versatile`) with JSON mode.
   * Extract: `title_en`, `title_hi`, `material`, `story_en`, and bullet points.
4. **Verify Your Work:**
   * Simply re-run `python test_kartik.py` anytime to see your outputs!

---

### 📊 4. For Ishaan Anand (ML / Pricing & Market Linkage)
> **Goal:** Build the ethical pricing engine that guarantees fair artisan wages and recommends institutional B2B buyers. You do NOT need to touch the web server!

#### How to Start (Step-by-Step):
1. **Run Your 1-Click Sandbox Test:**
   * Open terminal and run:
     ```bash
     cd backend
     python test_ishaan.py
     ```
2. **Task A — Ethical Pricing Math (`backend/app/services/pricing_engine.py`):**
   * **Guaranteed Artisan Wage:** $	ext{Labor Hours} 	imes ₹100/	ext{hr}$
   * **Cost Floor:** $	ext{Material} + 	ext{Labor Wage} + ₹50	ext{ (Packaging)}$
   * **Category Multipliers:** Handloom ($1.45	imes$), Pottery ($1.35	imes$), Metal/Dokra ($1.50	imes$)
   * **Wholesale Bulk Price:** $	ext{Cost Floor} 	imes 1.18$
3. **Task B — B2B Buyer Matcher:**
   * Implement `match_b2b_buyers()` to return matching institutional buyers (Tribes India, FabIndia).
4. **Verify Your Work:**
   * Run `python test_ishaan.py` to confirm your calculations!

---

### 🎖️ 5. For Jatin (DevOps, Integrations & Pitch Lead)
> **Goal:** External commerce connections, repository health, and directing the live SIH presentation.

#### What You Own:
1. **External Commerce Linkages (`backend/app/services/export_service.py`):**
   * Maintain the ONDC Beckn Protocol JSON schema.
   * Generate dynamic UPI payment QR codes (`upi://pay?pa=...`).
   * Generate printable A4 Mela Standee PDFs using ReportLab.
2. **Code Integration & Review:**
   * Pair with Prakriti & Saira on Frontend code, and Anikeat on Backend code.
   * Review teammate Pull Requests and merge into `main`.
3. **Live SIH Demo Kit:**
   * Maintain the 3 physical craft items (Brass lamp, Silk scarf, Clay pot) for the live booth pitch.

---

## 🚀 How We Merge Code (The Conflict-Free Ritual)

When your code is working and your sandbox test passes:
```bash
# 1. Save and commit:
git add .
git commit -m "feat: completed my module"

# 2. Push to GitHub:
git push origin <your-branch-name>

# 3. Open a Pull Request:
# Jatin will review and merge it cleanly into main!
```

Let's build a championship prototype! 🇮🇳
