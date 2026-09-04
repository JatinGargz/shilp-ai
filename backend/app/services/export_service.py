import io
import os
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_upi_qr_bytes(upi_id: str, payee_name: str, amount: float) -> bytes:
    payload = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount:.2f}&cu=INR"
    qr = qrcode.make(payload)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

def generate_ondc_beckn_json(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    return {
        "context": {
            "domain": "nic2004:52110",
            "country": "IND",
            "city": "std:080",
            "action": "on_search",
            "core_version": "0.9.3",
            "bap_id": "ondc.buyer.app",
            "bpp_id": "shilpai.mosje.bpp"
        },
        "message": {
            "catalog": {
                "bpp/descriptor": {
                    "name": "SHILP AI MoSJE Artisan Cluster",
                    "short_desc": "Government of India supported marginalized craft network"
                },
                "bpp/providers": [
                    {
                        "id": "provider_mosje_01",
                        "descriptor": {
                            "name": "National Scheduled Castes & Backward Classes Artisan Network"
                        },
                        "items": [
                            {
                                "id": product_id,
                                "descriptor": {
                                    "name": catalog.get("title_en", "Handcrafted Craft"),
                                    "short_desc": catalog.get("story_en", "Authentic Indian Art"),
                                    "images": [image_url]
                                },
                                "price": {
                                    "currency": "INR",
                                    "value": str(pricing.get("recommended_retail_price", "0"))
                                },
                                "category_id": catalog.get("craft_type", "Handicrafts"),
                                "matched": True
                            }
                        ]
                    }
                ]
            }
        }
    }

def generate_mela_standee_pdf(product_id: str, title: str, craft: str, price: float, artisan_name: str) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#D9531E'), alignment=1, spaceAfter=8)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#555555'), alignment=1, spaceAfter=16)
    prod_style = ParagraphStyle('Prod', parent=styles['Heading2'], fontSize=18, textColor=colors.HexColor('#1F2937'), alignment=1, spaceAfter=8)
    price_style = ParagraphStyle('Price', parent=styles['Heading1'], fontSize=28, textColor=colors.HexColor('#2E7D32'), alignment=1, spaceAfter=16)
    
    elements = [
        Paragraph("SHILP AI (शिल्प)", title_style),
        Paragraph("Ministry of Social Justice & Empowerment (MoSJE) Beneficiary Stall", sub_style),
        Spacer(1, 10),
        Paragraph(f"<b>{title}</b>", prod_style),
        Paragraph(f"Traditional Heritage: {craft} | Master Artisan: {artisan_name}", sub_style),
        Spacer(1, 15),
        Paragraph(f"Certified Fair Price: Rs. {price:.0f}", price_style),
        Spacer(1, 10)
    ]
    
    qr_bytes = generate_upi_qr_bytes(f"{product_id}@upi", artisan_name, price)
    qr_img = RLImage(io.BytesIO(qr_bytes), width=190, height=190)
    elements.append(qr_img)
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("<b>Scan with any UPI App (GPay / PhonePe / Paytm) to Pay Directly to Artisan</b>", sub_style))
    elements.append(Paragraph("Available year-round on Open Network for Digital Commerce (ONDC)", sub_style))
    
    doc.build(elements)
    return buf.getvalue()
