from config import COMPROBANTES
from utils import generar_comprobante

def generar_comprobante3(name: str, phone: str, value: int) -> str:
    config = COMPROBANTES["comprobante3"]
    return generar_comprobante(name, phone, value, config, ajuste_x=-140)