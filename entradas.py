import json
from datetime import date


class EntradaError(Exception):
    def __init__(self, code, mensaje):
        super().__init__(mensaje)
        self.code = code
        self.mensaje = mensaje


PRECIOS = {
    "GENERAL": 18999.90,
    "VIP": 32500.50,
    "ESTUDIANTE": 12999.50,
}

SECTORES = ["PISTA", "PLATEA", "PALCO"]

CODIGOS = {
    "PROMO2026": {"tipo": "porcentaje", "valor": 0.25, "vence": date(2026, 12, 15)},
    "AMIGO": {"tipo": "fijo", "valor": 5000, "minimo": 40000},
}

ENTREGAS = {"RETIRO": 0, "MOTO": 2000, "CORREO": 3500}


def validar_entrada(entrada):
    entrada["sector"] = entrada["sector"].upper()
    if entrada["sector"] not in SECTORES:
        EntradaError("SECTOR_INVALIDO", f"Sector inválido: {entrada['sector']}")
    if not (1 <= entrada["cantidad"] < 8):
        raise EntradaError("CANTIDAD_INVALIDA", f"Cantidad inválida: {entrada['cantidad']}")


def calcular_subtotal(entradas):
    subtotal = 0
    for entrada in entradas:
        validar_entrada(entrada)
        precio = entrada.get("precio") or PRECIOS.get(entrada["tipo"].upper(), 0)
        subtotal += precio * entrada["cantidad"]
    return round(subtotal, 2)


def calcular_descuento(subtotal, cantidad_entradas, codigo=None, fecha=None):
    if fecha is None:
        fecha = date.today()
    descuento = 0
    if cantidad_entradas > 6:
        descuento += subtotal * 0.12
    if codigo != None:
        codigo = codigo.strip()
        if codigo not in CODIGOS:
            raise EntradaError("CODIGO_INVALIDO", f"Código inválido: {codigo}")
        datos = CODIGOS[codigo]
        if datos["tipo"] == "porcentaje":
            if not fecha < datos["vence"]:
                raise EntradaError("CODIGO_VENCIDO", "El código está vencido")
            descuento += subtotal * datos["valor"]
        else:
            if subtotal < datos["minimo"]:
                raise EntradaError("CODIGO_MINIMO_NO_ALCANZADO", "El subtotal no alcanza el mínimo")
            descuento += datos["valor"]
    return round(descuento, 2)


def calcular_cargo(base, entrega):
    entrega = entrega.strip().upper()
    if entrega not in ENTREGAS:
        raise EntradaError("ENTREGA_INVALIDA", f"Entrega inválida: {entrega}")
    if base >= 80000:
        return 0
    return ENTREGAS[entrega]


def calcular_total(entradas, entrega, codigo=None, fecha=None):
    subtotal = calcular_subtotal(entradas)
    cantidad = sum(e["cantidad"] for e in entradas)
    descuento = calcular_descuento(subtotal, cantidad, codigo, fecha)
    cargo = calcular_cargo(subtotal, entrega)
    total = subtotal - descuento + cargo
    return {
        "subtotal": subtotal,
        "descuento": descuento,
        "cargo": cargo,
        "total": round(total, 2),
    }
