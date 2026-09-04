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

def format_amazon_karigar_feed(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    price = pricing.get("recommended_retail_price", 2900.0)
    clean_id = product_id.replace('shilp_', '').replace('prod_', '').upper()[:6]
    asin = f"B0{clean_id}9K"
    return {
        "channel": "Amazon Karigar",
        "program": "Amazon Karigar — Crafting Handloom India",
        "asin": asin,
        "status": "LIVE",
        "storefront_url": f"https://www.amazon.in/karigar/{product_id}",
        "title": catalog.get("title_en", "Handcrafted Heritage Artifact"),
        "price_inr": price,
        "mrp_inr": round(price * 1.45, -1),
        "commission_rate": "5% (Subsidized under Karigar MoU)",
        "fulfillment_mode": "Amazon Easy Ship / Seller Self-Ship",
        "badge": "Amazon Handcrafted Guarantee",
        "bullets": [
            f"Authentic Handcrafted: {catalog.get('craft_type', 'Indian Handloom')}",
            f"Pure Traditional Material: {catalog.get('material', 'Natural Material')}",
            "MoSJE Certified Artisan Partner (PM Vishwakarma Program)",
            "1080p Studio Quality Certified Listing",
            "100% Direct to Artisan Proceeds"
        ]
    }

def format_flipkart_samarth_feed(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    price = pricing.get("recommended_retail_price", 2900.0)
    clean_id = product_id.replace('shilp_', '').replace('prod_', '').upper()[:6]
    fsn = f"FSN{clean_id}44"
    return {
        "channel": "Flipkart Samarth",
        "program": "Flipkart Samarth (Empowering Indian Weavers)",
        "fsn": fsn,
        "status": "LIVE",
        "storefront_url": f"https://www.flipkart.com/samarth/{product_id}",
        "title": catalog.get("title_en", "Handcrafted Heritage Artifact"),
        "price_inr": price,
        "commission_rate": "0% Commission for 6 Months",
        "vertical": catalog.get("craft_type", "EthnicCraft"),
        "brand": "SHILP-MoSJE-Artisans",
        "badge": "Flipkart Samarth Verified",
        "warehouse": "Varanasi / Cluster Local Hub"
    }

def format_gem_procurement_feed(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    wholesale = pricing.get("wholesale_b2b_price", 2320.0)
    clean_id = product_id.replace('shilp_', '').replace('prod_', '').upper()[:6]
    gem_id = f"GEM/2026/SARAS/{clean_id}"
    return {
        "channel": "GeM (Govt e-Marketplace)",
        "program": "The Saras Collection & Tribal Procurement",
        "gem_item_id": gem_id,
        "status": "TENDER_ELIGIBLE",
        "storefront_url": f"https://gem.gov.in/saras/{product_id}",
        "title": catalog.get("title_en", "Handcrafted Heritage Artifact"),
        "institutional_price_inr": wholesale,
        "minimum_order_qty": 25,
        "category_code": "53101500 (Handicrafts & Artisan Wares)",
        "procurement_policy": "Direct PSU / Ministry Purchase under GFR Rule 149 (4% Mandated Quota)",
        "badge": "MoSJE Verified Public Procurement Partner"
    }

def format_etsy_global_feed(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    price_inr = pricing.get("recommended_retail_price", 2900.0)
    price_usd = round(price_inr / 85.0, 2)
    clean_id = product_id.replace('shilp_', '').replace('prod_', '').upper()[:6]
    return {
        "channel": "Etsy Global Export",
        "program": "Etsy India Handcrafted Exports",
        "listing_id": f"ETSY-{clean_id}-GLOBAL",
        "status": "INTERNATIONAL_LIVE",
        "storefront_url": f"https://www.etsy.com/shop/ShilpArtisans/{clean_id}",
        "title": catalog.get("title_en", "Handcrafted Heritage Artifact"),
        "price_usd": f"${price_usd:.2f} USD",
        "price_inr_equivalent": f"₹ {price_inr:,.0f}",
        "shipping_coverage": "United States, United Kingdom, European Union, Australia",
        "logistics_partner": "India Post International / DHL eCommerce",
        "badge": "Authentic Indian Cultural Heritage Export"
    }

def publish_to_all_channels(product_id: str, catalog: dict, pricing: dict, image_url: str) -> dict:
    return {
        "product_id": product_id,
        "timestamp": "2026-09-04T17:25:00Z",
        "total_channels_connected": 5,
        "channels": {
            "ondc": generate_ondc_beckn_json(product_id, catalog, pricing, image_url),
            "amazon_karigar": format_amazon_karigar_feed(product_id, catalog, pricing, image_url),
            "flipkart_samarth": format_flipkart_samarth_feed(product_id, catalog, pricing, image_url),
            "gem_procurement": format_gem_procurement_feed(product_id, catalog, pricing, image_url),
            "etsy_global": format_etsy_global_feed(product_id, catalog, pricing, image_url)
        }
    }

