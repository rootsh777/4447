from config import COMPROBANTES
from utils import generar_comprobante

def generar_comprobante4(phone: str, value: int) -> str:
    config = COMPROBANTES["comprobante4"]
    # Se usa un ajuste fijo para desplazar un poquito a la derecha, por ejemplo, -100
    return generar_comprobante("", phone, value, config, ajuste_x=-100)