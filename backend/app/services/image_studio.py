import io
import os
from PIL import Image, ImageEnhance

def enhance_craft_image(image_bytes: bytes, prod_id: str, static_dir: str) -> str:
    try:
        raw = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    except Exception:
        raw = Image.new("RGBA", (800, 800), (200, 100, 50, 255))
    
    try:
        from rembg import remove
        nobg = remove(raw)
    except Exception:
        nobg = raw

    try:
        nobg = ImageEnhance.Color(nobg).enhance(1.18)
        nobg = ImageEnhance.Contrast(nobg).enhance(1.08)
    except Exception:
        pass

    canvas = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
    nobg.thumbnail((860, 860), Image.Resampling.LANCZOS)
    x = (1080 - nobg.width) // 2
    y = (1080 - nobg.height) // 2
    canvas.paste(nobg, (x, y), nobg)
    
    filename = f"studio_{prod_id}.jpg"
    filepath = os.path.join(static_dir, "studio", filename)
    canvas.convert("RGB").save(filepath, format="JPEG", quality=92)
    return f"/static/studio/{filename}"
