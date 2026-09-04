# 🇮🇳 SHILP AI — Smart Handicraft Intelligence & Linkage Platform
### Problem Statement: SIH26090 | Ministry of Social Justice and Empowerment (MoSJE)

A voice-first AI virtual business manager empowering marginalized artisans to photograph, catalog, price, and sell their crafts on ONDC and B2B marketplaces.

---

## 👥 Team Roles & Responsibilities

| Role | Members | Core Ownership |
| :--- | :--- | :--- |
| **UI/UX & Design** | **Prakriti & Saira** | Figma wireframes, design system, color palette, visual layouts, and user experience |
| **Frontend Technical** | **Jatin + Prakriti & Saira** | Technical web implementation, state management, API integration, and mobile simulator |
| **Backend & Database** | **Anikeat + Jatin** | FastAPI server, SQLAlchemy database models, CRUD endpoints, and AI pipeline orchestration |
| **AI / GenAI & Vision** | **Kartik Dhiman** | Image studio background removal (`rembg`), Whisper STT, and Groq Llama-3 multilingual catalog |
| **ML & Pricing** | **Ishaan Anand** | Dynamic wage-floor pricing algorithm, craft category markups, and B2B buyer recommendation |
| **DevOps & Integrations** | **Jatin** | ONDC Beckn schema, UPI QR generator, printable Mela Standee PDF, and SIH pitch presentation |

---

## ⚡ Quick Start for Team Members

### 1. Backend Setup (Anikeat, Jatin, Kartik, Ishaan)
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows (or source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view the interactive Swagger API documentation.

### 2. Frontend Dual-Screen Suite (Prakriti, Saira, Jatin)
Double-click `frontend/index.html` in your file explorer to open the interactive live suite in Chrome.
Toggle between **Artisan Mobile (PWA)**, **Ministry Central Dashboard**, and the **Dual-Screen Live Booth View**.

### 3. Isolated AI & ML Test Sandboxes
* **Kartik Dhiman:** `python backend/test_kartik.py`
* **Ishaan Anand:** `python backend/test_ishaan.py`
