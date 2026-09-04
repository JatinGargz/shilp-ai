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

## 🛡️ Zero-Conflict Team Ownership Map
Every team member works **only inside their assigned files**. Because no two people edit the same file, Git merge conflicts are virtually impossible.

```
shilp-ai/
│
├── 🎨 FRONTEND WORKSPACE ──────────> Prakriti & Saira
│   └── frontend/index.html          (Unified Web App: Mobile Simulator + Ministry Dashboard)
│
├── ⚙️ BACKEND & DATABASE WORKSPACE ──> Anikeat
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

If you have never worked on a group coding project before, follow these 4 simple steps:

1. **Install Required Software:**
   * Download and install **[VS Code](https://code.visualstudio.com/)**.
   * Download and install **[Python 3.10+](https://www.python.org/downloads/)** (Check the box that says *"Add python.exe to PATH"* during installation!).
   * Download and install **[Git](https://git-scm.com/)**.
2. **Open the Project:**
   * Open VS Code $\rightarrow$ `File` $\rightarrow$ `Open Folder...` $\rightarrow$ Select the `shilp-ai` folder.
3. **Open Terminal in VS Code:**
   * Press `Ctrl + ~` (or go to menu: `Terminal` $\rightarrow$ `New Terminal`).
4. **Create Your Personal Branch:**
   * Run the command matching your name:
     ```bash
     # Prakriti & Saira:
     git checkout -b frontend/dual-view-suite

     # Anikeat:
     git checkout -b backend/database-apis

     # Kartik Dhiman:
     git checkout -b ai/vision-voice-pipeline

     # Ishaan Anand:
     git checkout -b ml/pricing-engine
     ```

---

## 👤 Beginner Playbook for Each Teammate

---

### 🎨 1. For Prakriti & Saira (UI/UX & Frontend)
> **Goal:** Design and polish the user interface. You don't need any complex frameworks to start!

#### How to Start (Step-by-Step):
1. **View the Working App Right Now:**
   * Double-click [`frontend/index.html`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/frontend/index.html) in your file explorer. It will open directly in Google Chrome!
   * Notice the 3 buttons at the top:
     * **Artisan Mobile (PWA):** Shows the mobile phone mockup frame.
     * **Ministry Central Dashboard:** Shows the executive analytics view.
     * **Dual-Screen Live Booth View:** Shows both side-by-side (our hackathon presentation view!).
2. **Test the Live Connection:**
   * Click the big orange microphone button inside the phone frame. It will call the backend at `http://localhost:8000/api/v1/media/process-raw` and instantly display the 4K studio image, generated title, fair price, and WhatsApp card!
3. **What You Need to Polish in `frontend/index.html`:**
   * **Colors:** Use earthy, cultural Indian tones (Terracotta Orange `#D9531E`, Heritage Saffron `#E07A5F`, Deep Slate `#1F2937`, Warm Cream `#FFFBF5`).
   * **Artisan Flow:** Add an image upload preview slider (Before vs. After).
   * **Ministry View:** Add a state selector dropdown (Uttar Pradesh, Chhattisgarh, Rajasthan, Gujarat).
   * **Audio Player:** Add an audio `<audio>` player element that automatically plays the spoken Hindi confirmation.

---

### ⚙️ 2. For Anikeat (Backend & Database)
> **Goal:** Run the FastAPI backend server, create database tables, and store product records.

#### How to Start (Step-by-Step):
1. **Start the Backend Server:**
   * Open the VS Code terminal and run:
     ```bash
     cd backend
     python -m uvicorn app.main:app --reload --port 8000
     ```
2. **Open the Interactive API Docs:**
   * Open your browser and go to **[http://localhost:8000/docs](http://localhost:8000/docs)**.
   * You will see the interactive Swagger documentation where you can test any API with 1 click!
3. **Your Files to Work On:**
   * Open [`backend/app/models/models.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/models/models.py):
     * Review the SQLAlchemy classes: `Artisan`, `Product`, `ProductMedia`, `ProductPricing`, and `B2BEnquiry`.
     * Add any extra fields you need (e.g., `phone_number`, `state`, `cluster`).
   * Open [`backend/app/api/`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/api/):
     * Implement a route to save uploaded camera photos to disk (`uploads/images/`).
     * Implement a route to query products filtered by craft category (`/api/v1/products?category=textiles`).

---

### 🧠 3. For Kartik Dhiman (AI / GenAI & Vision)
> **Goal:** Remove backgrounds from craft photos and generate bilingual e-commerce listings from voice notes. You do NOT need to touch the web server to develop your code!

#### How to Start (Step-by-Step):
1. **Run Your 1-Click Sandbox Test:**
   * Open terminal and run:
     ```bash
     cd backend
     python test_kartik.py
     ```
   * It will instantly test your functions and print the outputs.
2. **Task A — Build the Image Studio (`backend/app/services/image_studio.py`):**
   * Open [`backend/app/services/image_studio.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/image_studio.py).
   * Write the code to:
     ```python
     from rembg import remove
     from PIL import Image, ImageEnhance
     import io

     def enhance_craft_image(image_bytes: bytes) -> bytes:
         raw = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
         nobg = remove(raw)  # Strips cluttered background
         
         # Boost craft color saturation (+15%)
         nobg = ImageEnhance.Color(nobg).enhance(1.15)
         
         # Place on 1080x1080 white canvas
         canvas = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
         nobg.thumbnail((850, 850), Image.Resampling.LANCZOS)
         canvas.paste(nobg, ((1080 - nobg.width)//2, (1080 - nobg.height)//2), nobg)
         
         buf = io.BytesIO()
         canvas.convert("RGB").save(buf, format="JPEG", quality=92)
         return buf.getvalue()
     ```
3. **Task B — Voice to Catalog (`backend/app/services/catalog_engine.py`):**
   * Get a free API key from **[console.groq.com](https://console.groq.com/)**.
   * Call `llama-3.3-70b-versatile` with JSON response mode to extract: `title_en`, `title_hi`, `material`, `story_en`, and bullet points.
4. **Verify Your Work:**
   * Simply run `python test_kartik.py` again to see your live code in action!

---

### 📊 4. For Ishaan Anand (ML / Pricing & Market Linkage)
> **Goal:** Build the ethical pricing engine that protects artisans from being cheated by middlemen. You do NOT need to touch the web server to develop your code!

#### How to Start (Step-by-Step):
1. **Run Your 1-Click Sandbox Test:**
   * Open terminal and run:
     ```bash
     cd backend
     python test_ishaan.py
     ```
   * It will calculate a sample Banarasi Silk pricing breakdown.
2. **Your File to Work On:**
   * Open [`backend/app/services/pricing_engine.py`](file:///C:/Users/Jatin/.gemini/antigravity/scratch/shilp-ai/backend/app/services/pricing_engine.py).
3. **Implement the 3 Rules:**
   * **Rule 1: Guaranteed Artisan Minimum Wage**:
     $$\text{Labor Wage} = \text{Labor Hours} \times ₹100/\text{hr}$$
   * **Rule 2: Cost Floor**:
     $$\text{Cost Floor} = \text{Material Cost} + \text{Labor Wage} + ₹50\text{ (Packaging)}$$
   * **Rule 3: Category Fair Markups**:
     * Textiles / Handloom: $1.45\times$
     * Pottery / Clay: $1.35\times$
     * Metal / Dokra: $1.50\times$
     * Woodcraft: $1.40\times$
   * **Rule 4: Wholesale B2B Price**:
     $$\text{Wholesale Price} = \text{Cost Floor} \times 1.18\text{ (for orders } \ge 25\text{ units)}$$
4. **Implement B2B Buyer Matching (`match_b2b_buyers()`):**
   * Return matching institutional buyers (e.g., Tribes India, FabIndia, Central Cottage Industries Emporium) based on craft category.
5. **Verify Your Work:**
   * Run `python test_ishaan.py` to confirm your formulas output clean, rounded numbers.

---

### 🎖️ 5. For Jatin (DevOps, Integrations & Pitch Lead)
> **Goal:** Manage the repository, connect external linkages (ONDC & WhatsApp), and direct the SIH presentation.

#### What You Own:
1. **External Exports (`backend/app/services/export_service.py`):**
   * ONDC Beckn Protocol JSON schema generation.
   * Dynamic UPI payment QR code generator (`upi://pay?pa=...`).
   * Printable A4 Mela Standee PDF with QR code using ReportLab.
2. **PR Merges:**
   * Review Pull Requests from teammates, run `python backend/tests/test_api.py` to verify, and merge into `main`.
3. **Physical Demo Kit:**
   * Keep 3 real craft items on the booth table (Brass lamp, Silk scarf, Clay pot).

---

## 🚀 How We Merge Code (The Conflict-Free Ritual)

When you finish your tasks and your sandbox test passes:
```bash
# 1. Save and commit your changes:
git add .
git commit -m "feat: completed my assigned module"

# 2. Push your branch to GitHub:
git push origin <your-branch-name>

# 3. Open a Pull Request on GitHub:
# Jatin will review and merge it cleanly into main!
```

Let's build a championship prototype! 🇮🇳
