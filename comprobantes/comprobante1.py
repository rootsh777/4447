from config import COMPROBANTES
from utils import generar_comprobante

def generar_comprobante1(name: str, phone: str, value: int) -> str:
    config = COMPROBANTES["comprobante1"]
    # Se usa un ajuste fijo para mover el texto más a la izquierda, por ejemplo, -200
    return generar_comprobante(name, phone, value, config, ajuste_x=-200)