from config import COMPROBANTES
from utils import generar_comprobante

def generar_movimiento(name: str, value: int) -> str:
    config = COMPROBANTES["movimientos"]
    return generar_comprobante(name, "", value, config)