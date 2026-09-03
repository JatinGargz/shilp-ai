# 🇮🇳 SHILP AI — Smart Handicraft Intelligence & Linkage Platform
### Problem Statement: SIH26090 | Ministry of Social Justice and Empowerment (MoSJE)

A voice-first AI virtual business manager empowering marginalized artisans to photograph, catalog, price, and sell their crafts on ONDC and B2B marketplaces.

---

## ⚡ Quick Start for Team Members

### 1. Backend Setup (Anikeat, Kartik, Ishaan)
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view the interactive Swagger API documentation.

### 2. Frontend Setup (Prakriti & Saira)
Connect your mobile screens and web dashboard directly to `http://localhost:8000/api/v1/media/process-raw`.
The server is already running with mock responses matching the frozen contract!

---

## 👥 Ownership & Key Modules
* **Prakriti & Saira:** `frontend-mobile/` (Voice-first UI) & `frontend-admin/` (Ministry Dashboard)
* **Anikeat:** `backend/app/main.py`, database models & API endpoints
* **Kartik Dhiman:** `backend/app/services/image_studio.py` (rembg/OpenCV) & Whisper/LLM cataloging
* **Ishaan Anand:** `backend/app/services/pricing_engine.py` (ethical pricing formula)
* **Jatin:** `backend/app/services/export_service.py` (ONDC Beckn & UPI QR generator) & SIH Pitch
