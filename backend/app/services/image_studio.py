import io
from PIL import Image, ImageEnhance

def enhance_craft_image(image_bytes: bytes) -> bytes:
    raw = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    try:
        from rembg import remove
        nobg = remove(raw)
    except Exception as e:
        nobg = raw

    try:
        nobg = ImageEnhance.Color(nobg).enhance(1.15)
    except Exception:
        pass

    canvas = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
    nobg.thumbnail((850, 850), Image.Resampling.LANCZOS)
    x = (1080 - nobg.width) // 2
    y = (1080 - nobg.height) // 2
    canvas.paste(nobg, (x, y), nobg)
    
    output = io.BytesIO()
    canvas.convert("RGB").save(output, format="JPEG", quality=92)
    return output.getvalue()
