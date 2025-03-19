import os
import logging
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont
from config import FONT_PATH

def validar_archivo(path: str) -> bool:
    if not os.path.exists(path):
        logging.error(f"Archivo no encontrado: {path}")
        return False
    return True

def obtener_fecha_general() -> tuple[str, str]:
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    utc_now = datetime.now(pytz.utc)
    colombia_tz = pytz.timezone("America/Bogota")
    hora_colombiana = utc_now.astimezone(colombia_tz)
    dia = f"{hora_colombiana.day:02d}"
    mes = meses[hora_colombiana.month - 1]
    anio = hora_colombiana.year
    hora = hora_colombiana.strftime("%I:%M %p").lower()
    hora = hora.replace("am", "a. m.").replace("pm", "p. m.")
    return f"{dia} de {mes} de {anio}", f"a las {hora}"

def formatear_nombre(nombre: str, comprobante: str) -> str:
    return nombre.title()

def formatear_telefono(telefono: str, comprobante: str) -> str:
    telefono = telefono.replace(" ", "")
    if len(telefono) == 10:
        return f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}"
    return telefono

def formatear_valor(valor: int) -> str:
    return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def generar_comprobante(nombre: str, telefono: str, valor: int, config: dict, ajuste_x: int = 0, cc: str = "") -> str:
    template_path = config["template"]
    output_path = config["output"]
    styles = config["styles"]

    if not os.path.exists(template_path) or not os.path.exists(FONT_PATH):
        raise FileNotFoundError("Archivo de plantilla o fuente no encontrado")

    escala = 3
    img = Image.open(template_path)
    img = img.resize((img.width * escala, img.height * escala), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)

    fecha_linea1, fecha_linea2 = obtener_fecha_general()
    valor_formateado = formatear_valor(valor)
    ajuste_fecha_y = -25

    for key, style in styles.items():
        font = ImageFont.truetype(FONT_PATH, size=style["size"] * escala)
        if key == "fecha":
            if output_path == "comprobante5_generado.png":
                continue
            pos_y_base = style["pos"][1] * escala + ajuste_fecha_y * escala
            bbox1 = draw.textbbox((0, 0), fecha_linea1, font=font)
            text_width1 = bbox1[2] - bbox1[0]
            pos_x1 = img.width - text_width1 - 20 + ajuste_x
            draw.text((pos_x1, pos_y_base), fecha_linea1, font=font, fill=style["color"])
            bbox2 = draw.textbbox((0, 0), fecha_linea2, font=font)
            text_width2 = bbox2[2] - bbox2[0]
            pos_x2 = img.width - text_width2 - 20 + ajuste_x
            pos_y2 = pos_y_base + font.size + 5
            draw.text((pos_x2, pos_y2), fecha_linea2, font=font, fill=style["color"])
            continue

        if key == "nombre":
            texto = formatear_nombre(nombre, "comprobante")
        elif key == "telefono":
            texto = formatear_telefono(telefono, "comprobante")
        elif key == "valor1":
            texto = valor_formateado
        else:
            continue

        bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = bbox[2] - bbox[0]
        pos_x = img.width - text_width - 20 + ajuste_x
        pos_y = style["pos"][1] * escala
        draw.text((pos_x, pos_y), texto, font=font, fill=style["color"])

    if output_path == "comprobante5_generado.png":
        cc_style = styles.get("cc")
        if cc_style:
            font = ImageFont.truetype(FONT_PATH, size=cc_style["size"] * escala)
            pos_x = cc_style["pos"][0] * escala + ajuste_x
            pos_y = cc_style["pos"][1] * escala
            draw.text((pos_x, pos_y), cc, font=font, fill=cc_style["color"])

    img.save(output_path, quality=99)
    return output_path