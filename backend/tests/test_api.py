import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_products_list():
    res = client.get("/api/v1/products")
    assert res.status_code == 200
    data = res.json()
    assert "products" in data
    assert data["count"] >= 3

def test_process_raw_mock():
    res = client.post("/api/v1/media/process-raw", data={
        "craft_category": "pottery",
        "material_cost": "150",
        "labor_hours": "8",
        "transcript_hint": "Handmade clay pot"
    })
    assert res.status_code == 200
    data = res.json()
    assert "catalog" in data
    assert "pricing" in data

def test_mela_standee_pdf():
    res = client.get("/api/v1/products/shilp_101/mela-standee-pdf")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 500

def test_ondc_export():
    res = client.get("/api/v1/products/shilp_101/export/ondc")
    assert res.status_code == 200

def test_ministry_analytics():
    res = client.get("/api/v1/analytics/ministry")
    assert res.status_code == 200
