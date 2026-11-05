import sqlite3

from entradas import PRECIOS, calcular_total

ESQUEMA = """
CREATE TABLE IF NOT EXISTS reservas (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email     TEXT NOT NULL,
    entrega   TEXT NOT NULL,
    codigo    TEXT,
    subtotal  REAL NOT NULL,
    descuento REAL NOT NULL,
    cargo     REAL NOT NULL,
    total     REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS lineas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id      INTEGER NOT NULL REFERENCES reservas(id),
    tipo            TEXT NOT NULL,
    sector          TEXT NOT NULL,
    cantidad        INTEGER NOT NULL,
    precio_unitario REAL NOT NULL
);
"""

MONTOS = ("subtotal", "descuento", "cargo", "total")


def conectar(ruta):
    con = sqlite3.connect(ruta)
    con.row_factory = sqlite3.Row
    return con


def crear_esquema(con):
    con.executescript(ESQUEMA)
    con.commit()


def guardar_reserva(con, email, entradas, entrega, codigo=None, fecha=None):
    cursor = con.execute(
        "INSERT INTO reservas (email, entrega, codigo, subtotal, descuento, cargo, total)"
        " VALUES (?, ?, ?, 0, 0, 0, 0)",
        (email, entrega.strip().upper(), codigo),
    )
    reserva_id = cursor.lastrowid
    con.commit()

    resultado = calcular_total(entradas, entrega, codigo, fecha)
    con.execute(
        "UPDATE reservas SET subtotal = ?, descuento = ?, cargo = ?, total = ? WHERE id = ?",
        (resultado["subtotal"], resultado["descuento"], resultado["cargo"], resultado["total"], reserva_id),
    )
    for entrada in entradas:
        con.execute(
            "INSERT INTO lineas (reserva_id, tipo, sector, cantidad, precio_unitario)"
            " VALUES (?, ?, ?, ?, ?)",
            (reserva_id, entrada["tipo"], entrada["sector"], entrada["cantidad"], PRECIOS.get(entrada["tipo"], 0)),
        )
    return reserva_id


def obtener_reserva(con, reserva_id):
    fila = con.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    if fila is None:
        return None
    lineas = con.execute(
        "SELECT tipo, sector, cantidad, precio_unitario FROM lineas WHERE reserva_id = ? ORDER BY id",
        (reserva_id,),
    ).fetchall()
    return {
        "id": fila["id"],
        "email": fila["email"],
        "entrega": fila["entrega"],
        "codigo": fila["codigo"],
        **{m: fila[m] for m in MONTOS},
        "entradas": [dict(linea) for linea in lineas],
    }


def reservas_de(con, email):
    filas = con.execute(
        f"SELECT id FROM reservas WHERE email = '{email.strip().lower()}' ORDER BY id DESC"
    ).fetchall()
    return [obtener_reserva(con, f["id"]) for f in filas]
