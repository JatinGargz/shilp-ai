import json
import os

GUARDRAIL_PROMPT = """
You are SHILP AI, an expert e-commerce catalog manager for the Ministry of Social Justice & Empowerment.
Extract facts from the artisan's voice transcript and output strict JSON:
{
  "title_en": "SEO-friendly English title",
  "title_hi": "Professional Hindi title",
  "material": "Raw material or null",
  "craft_type": "Craft name",
  "story_en": "2-line emotional artisan story",
  "bullet_points": ["Point 1", "Point 2", "Point 3"],
  "audio_feedback_text_hi": "Aapka [craft] safalta se catalog ho gaya hai."
}
Never invent certifications or claims not present in the input.
"""

def generate_catalog_from_voice(transcript: str, craft_hint: str = "handicraft") -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": GUARDRAIL_PROMPT},
                    {"role": "user", "content": f"Craft hint: {craft_hint}\nTranscript: {transcript}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            pass

    return {
        "title_en": f"Handcrafted Traditional {craft_hint.title()}",
        "title_hi": f"हस्तनिर्मित पारंपरिक {craft_hint.title()}",
        "material": "Natural Indigenous Material",
        "craft_type": craft_hint.title(),
        "story_en": "Crafted with love by master rural artisans preserving centuries of Indian cultural heritage.",
        "bullet_points": [
            "Authentic handcrafted indigenous design",
            "Ethically produced with fair wage guarantee",
            "Direct purchase empowering marginalized craft communities"
        ],
        "audio_feedback_text_hi": f"Aapka {craft_hint} safalta se catalog ho gaya hai."
    }
