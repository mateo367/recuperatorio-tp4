from datetime import date
from decimal import Decimal

import pytest

import reservas
from entradas import EntradaError

HOY_VIGENTE = date(2026, 10, 1)


@pytest.fixture
def ruta(tmp_path):
    return str(tmp_path / "entradas.db")


@pytest.fixture
def con(ruta):
    conexion = reservas.conectar(ruta)
    reservas.crear_esquema(conexion)
    yield conexion
    conexion.close()


def entrada(tipo="GENERAL", sector="PISTA", cantidad=1, **extra):
    return {"tipo": tipo, "sector": sector, "cantidad": cantidad, **extra}


def contar(ruta, tabla):
    otra = reservas.conectar(ruta)
    try:
        return otra.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    finally:
        otra.close()


def test_un_id_inexistente_devuelve_none(con):
    assert reservas.obtener_reserva(con, 999) is None
