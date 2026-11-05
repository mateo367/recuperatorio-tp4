from datetime import date

import pytest

from entradas import (
    EntradaError,
    calcular_cargo,
    calcular_descuento,
    calcular_subtotal,
    calcular_total,
    validar_entrada,
)

HOY_VIGENTE = date(2026, 10, 1)


def entrada(tipo="GENERAL", sector="PISTA", cantidad=1, **extra):
    return {"tipo": tipo, "sector": sector, "cantidad": cantidad, **extra}


def codigo_de_error(funcion, *args):
    with pytest.raises(EntradaError) as error:
        funcion(*args)
    return error.value.code


def test_cantidad_cero_es_invalida():
    assert codigo_de_error(validar_entrada, entrada(cantidad=0)) == "CANTIDAD_INVALIDA"
