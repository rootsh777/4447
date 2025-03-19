from config import COMPROBANTES
from utils import generar_comprobante

def generar_comprobante5(name: str, phone: str, value: int, cc: str) -> str:
    config = COMPROBANTES["comprobante5"]
    return generar_comprobante(name, phone, value, config, ajuste_x=-140, cc=cc)