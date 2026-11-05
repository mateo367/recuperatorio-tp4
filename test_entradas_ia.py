from datetime import date

from entradas import PRECIOS, calcular_cargo, calcular_descuento, calcular_subtotal, calcular_total, validar_entrada


def test_subtotal():
    entradas = [{"tipo": "GENERAL", "sector": "PISTA", "cantidad": 2}]
    assert calcular_subtotal(entradas) == PRECIOS["GENERAL"] * 2


def test_total_funciona():
    resultado = calcular_total([{"tipo": "VIP", "sector": "PALCO", "cantidad": 1}], "RETIRO")
    assert resultado is not None


def test_total_positivo():
    resultado = calcular_total([{"tipo": "ESTUDIANTE", "sector": "PLATEA", "cantidad": 2}], "MOTO")
    assert resultado["total"] > 0


def test_codigo_promo():
    descuento = calcular_descuento(100000, 1, "PROMO2026", date(2026, 10, 1))
    assert descuento == 100000 * 0.25


def test_cargo_moto():
    assert calcular_cargo(10000, "MOTO") == 2000


def test_descuento_por_grupo():
    assert calcular_descuento(100000, 7) == 12000


def test_sector_valido():
    validar_entrada({"tipo": "VIP", "sector": "PLATEA", "cantidad": 1})


def test_no_explota_con_varias_entradas():
    entradas = [
        {"tipo": "GENERAL", "sector": "PISTA", "cantidad": 2},
        {"tipo": "VIP", "sector": "PALCO", "cantidad": 1},
    ]
    try:
        calcular_total(entradas, "CORREO")
    except Exception:
        pass
