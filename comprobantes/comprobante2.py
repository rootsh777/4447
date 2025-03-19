from config import COMPROBANTES
from utils import generar_comprobante

def generar_comprobante2(name: str, phone: str, value: int) -> str:
    config = COMPROBANTES["comprobante2"]
    return generar_comprobante(name, phone, value, config, ajuste_x=-140)