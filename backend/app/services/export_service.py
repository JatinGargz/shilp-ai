import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_upi_qr_bytes(upi_id: str, payee_name: str, amount: float) -> bytes:
    payload = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount:.2f}&cu=INR"
    try:
        import qrcode
        qr = qrcode.make(payload)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

def generate_ondc_beckn_json(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    return {
        "context": {
            "domain": "nic2004:52110",
            "country": "IND",
            "city": "std:080",
            "action": "on_search",
            "core_version": "0.9.3"
        },
        "message": {
            "catalog": {
                "bpp/descriptor": {
                    "name": "SHILP AI MoSJE Artisan Cluster",
                    "short_desc": "Government supported marginalized craft network"
                },
                "bpp/providers": [
                    {
                        "id": "provider_mosje_01",
                        "items": [
                            {
                                "id": product_id,
                                "descriptor": {
                                    "name": catalog.get("title_en", "Handcrafted Art"),
                                    "short_desc": catalog.get("story_en", "Authentic Indian Handloom"),
                                    "images": [image_url]
                                },
                                "price": {
                                    "currency": "INR",
                                    "value": str(pricing.get("recommended_retail_price", "0"))
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }

def generate_mela_standee_pdf(product_id: str, title: str, craft: str, price: float, artisan_name: str) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#D9531E'), alignment=1)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#555555'), alignment=1)
    price_style = ParagraphStyle('Price', parent=styles['Heading2'], fontSize=24, textColor=colors.HexColor('#2E7D32'), alignment=1)
    
    elements = [
        Paragraph("SHILP AI — Mela Direct Stall Display", header_style),
        Spacer(1, 10),
        Paragraph("Ministry of Social Justice & Empowerment (MoSJE) Beneficiary Stall", sub_style),
        Spacer(1, 20),
        Paragraph(f"<b>Product:</b> {title}", styles['Heading3']),
        Paragraph(f"<b>Craft Heritage:</b> {craft} | <b>Artisan:</b> {artisan_name}", styles['Normal']),
        Spacer(1, 20),
        Paragraph(f"Official Fair Price: Rs. {price:.0f}", price_style),
        Spacer(1, 15),
        Paragraph("Scan with any UPI App (GPay / PhonePe / Paytm) to Pay Directly", sub_style),
        Paragraph("Available year-round on ONDC Network", sub_style)
    ]
    doc.build(elements)
    return buf.getvalue()
