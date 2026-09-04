import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services.image_studio import enhance_craft_image
from app.services.catalog_engine import generate_catalog_from_voice

print("=" * 60)
print("  KARTIK'S AI PIPELINE SANDBOX TEST")
print("=" * 60)

sample_transcript = "Yeh pure Banarasi katan silk dupatta hai, haath se buna hua gold zari ke sath, do din lage banane me, 350 rupaye ka kacha mal laga."
print("\n[Testing Catalog Engine...]")
catalog_output = generate_catalog_from_voice(sample_transcript, craft_hint="Banarasi Silk Dupatta")

print("Generated English Title:", catalog_output.get("title_en"))
print("Generated Hindi Title:  ", catalog_output.get("title_hi"))
print("Generated Heritage Story:", catalog_output.get("story_en"))
print("Audio Confirmation Text:", catalog_output.get("audio_feedback_text_hi"))

print("\n[Testing Image Studio Pipeline...]")
sample_image_path = os.path.join(os.path.dirname(__file__), "..", "demo-assets", "sample-crafts", "sample_brass_diya.jpg")
if os.path.exists(sample_image_path):
    with open(sample_image_path, "rb") as f:
        raw_bytes = f.read()
    output_bytes = enhance_craft_image(raw_bytes)
    print(f"Enhanced Image Processed! Output size: {len(output_bytes)} bytes")
else:
    print("Sample craft photo not found, skipping image test.")

print("\n[SUCCESS] Kartik's test ran cleanly! Now edit backend/app/services/ to implement your code.")
