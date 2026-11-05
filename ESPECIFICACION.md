# Especificación — Entradas para la fiesta de egresados

Este documento es el contrato del sistema. Si el código y la especificación no
coinciden, el error está en el código.

---

## 1. El sistema

Tres módulos de Python:

| Módulo | Responsabilidad |
|---|---|
| `entradas.py` | Calcula el precio de una compra de entradas |
| `reservas.py` | Guarda las reservas en una base de datos SQLite |
| `api.py` | Recibe las reservas por HTTP |

Una **entrada** es un diccionario con tres claves:

```python
{"tipo": "VIP", "sector": "PALCO", "cantidad": 2}
```

Cualquier otra clave se ignora.

---

## 2. Funciones de `entradas.py`

```python
validar_entrada(entrada: dict) -> None
calcular_subtotal(entradas: list[dict]) -> Decimal
calcular_descuento(subtotal: Decimal, cantidad_entradas: int,
                   codigo: str | None = None, fecha: date | None = None) -> Decimal
calcular_cargo(base: Decimal, entrega: str) -> Decimal
calcular_total(entradas: list[dict], entrega: str,
               codigo: str | None = None, fecha: date | None = None) -> dict
```

`calcular_total` devuelve un diccionario con cuatro importes:

```python
{"subtotal": Decimal, "descuento": Decimal, "cargo": Decimal, "total": Decimal}
```

Todos los errores de negocio se informan con `EntradaError`:

```python
class EntradaError(Exception):
    code: str       # uno de los códigos de la sección 4
    mensaje: str    # texto para mostrar al usuario
```

Una entrada inválida nunca produce otro tipo de excepción.

### R1 — Tipos de entrada

| Tipo | Precio |
|---|---:|
| `GENERAL` | $ 18.999,90 |
| `VIP` | $ 32.500,50 |
| `ESTUDIANTE` | $ 12.999,50 |

- El tipo se reconoce sin distinguir mayúsculas y sin los espacios de
  alrededor: `" vip "` es `VIP`.
- Cualquier otro tipo → `TIPO_INEXISTENTE`.
- El precio es siempre el de esta tabla, aunque la entrada traiga otra clave,
  como `"precio"`.

### R2 — Sectores

Los sectores válidos son `PISTA`, `PLATEA` y `PALCO`. Se reconocen sin
distinguir mayúsculas y sin los espacios de alrededor. Cualquier otro sector →
`SECTOR_INVALIDO`.

### R3 — Cantidad

Un número entero entre 1 y 8, ambos inclusive. Un número no entero o un
booleano → `CANTIDAD_INVALIDA`.

### R4 — Lista de entradas

- Una lista vacía → `LISTA_VACIA`.
- Ninguna función modifica la lista ni las entradas que recibe.

### R5 — Descuento por grupo

12 % del subtotal si la compra tiene **6 entradas o más**. Se cuentan todas las
entradas, sumando las cantidades de todas las líneas.

### R6 — Códigos promocionales

| Código | Descuento | Condición |
|---|---|---|
| `PROMO2026` | 25 % del subtotal | Válido hasta el 15/12/2026 inclusive |
| `AMIGO` | $ 5.000,00 | Subtotal de $ 40.000,00 o más |

- Después del 15/12/2026, `PROMO2026` → `CODIGO_VENCIDO`.
- Con un subtotal menor a $ 40.000,00, `AMIGO` → `CODIGO_MINIMO_NO_ALCANZADO`.
- El código se reconoce sin distinguir mayúsculas y sin los espacios de
  alrededor.
- `None`, un texto vacío o un texto de solo espacios equivalen a no usar código.
- Cualquier otro código → `CODIGO_INVALIDO`.
- El descuento por grupo y el del código **no se suman**: se aplica el mayor.
- El descuento nunca supera el subtotal.
- Si no se recibe fecha, se usa la fecha del día en que se hace la llamada.

### R7 — Dinero

- Todos los importes son `Decimal`.
- Cada importe se redondea a 2 decimales con redondeo comercial: el medio
  centavo se redondea hacia arriba.

Ejemplo: el 25 % de $ 32.500,50 es $ 8.125,125, que se redondea a
**$ 8.125,13**.

### R8 — Cargo por entrega

| Entrega | Cargo |
|---|---:|
| `RETIRO` | $ 0,00 |
| `MOTO` | $ 2.000,00 |
| `CORREO` | $ 3.500,00 |

- La entrega se reconoce sin distinguir mayúsculas y sin los espacios de
  alrededor.
- Cualquier otra entrega → `ENTREGA_INVALIDA`.
- El cargo es **gratis** si la base es de $ 80.000,00 o más. La base es el
  subtotal **menos el descuento**.

### R9 — Total

```
total = subtotal − descuento + cargo
```

Ejemplo: 1 entrada VIP, entrega `MOTO`, código `PROMO2026`, fecha 01/10/2026:

| Subtotal | Descuento | Cargo | Total |
|---:|---:|---:|---:|
| 32.500,50 | 8.125,13 | 2.000,00 | 26.375,37 |

---

## 3. Orden de validación en `calcular_total`

Si una compra tiene más de un problema, se informa el primero según este
orden:

1. Lista vacía.
2. Cada entrada, en el orden en que aparece: tipo, sector, cantidad.
3. Código.
4. Entrega.

---

## 4. Códigos de error

| `code` | Cuándo |
|---|---|
| `TIPO_INEXISTENTE` | El tipo no está en la tabla de R1 |
| `SECTOR_INVALIDO` | El sector no es uno de los de R2 |
| `CANTIDAD_INVALIDA` | La cantidad no cumple R3 |
| `LISTA_VACIA` | La lista de entradas está vacía |
| `CODIGO_INVALIDO` | El código no existe |
| `CODIGO_VENCIDO` | `PROMO2026` después de su fecha |
| `CODIGO_MINIMO_NO_ALCANZADO` | `AMIGO` con un subtotal menor al mínimo |
| `ENTREGA_INVALIDA` | La entrega no es una de las de R8 |

---

## 5. Persistencia — `reservas.py`

```python
conectar(ruta: str) -> sqlite3.Connection
crear_esquema(con) -> None
guardar_reserva(con, email: str, entradas: list[dict], entrega: str,
                codigo: str | None = None, fecha: date | None = None) -> int
obtener_reserva(con, reserva_id: int) -> dict | None
reservas_de(con, email: str) -> list[dict]
```

`obtener_reserva` devuelve:

```python
{
    "id": 1, "email": "ana@mail.com", "entrega": "MOTO", "codigo": "PROMO2026",
    "subtotal": Decimal("32500.50"), "descuento": Decimal("8125.13"),
    "cargo": Decimal("2000.00"), "total": Decimal("26375.37"),
    "entradas": [
        {"tipo": "VIP", "sector": "PALCO", "cantidad": 1,
         "precio_unitario": Decimal("32500.50")},
    ],
}
```

Las entradas vuelven en el orden en que se guardaron.

### R10 — Reglas de persistencia

- `guardar_reserva` calcula los importes con `calcular_total`. Si eso lanza
  `EntradaError`, el error se propaga y **no queda nada guardado**: ni la
  reserva ni sus entradas.
- Cuando `guardar_reserva` termina, la reserva es **definitiva**: cualquier
  otra conexión a la misma base la ve completa, con todas sus entradas.
- Los montos que devuelve `obtener_reserva` son **idénticos** a los que calculó
  `entradas.py`: `Decimal`, mismo valor, sin ninguna pérdida.
- `precio_unitario` es el precio de la tabla de R1, nunca uno enviado por el
  cliente.
- Los datos se guardan normalizados: el email en minúscula y sin espacios
  alrededor; la entrega, el código, el tipo y el sector en mayúscula y sin
  espacios alrededor. Un código vacío o de solo espacios se guarda como `None`.
- `obtener_reserva` de un id que no existe devuelve `None`.
- `reservas_de` no distingue mayúsculas ni espacios en el email y devuelve las
  reservas **de la más reciente a la más antigua**. El email es un dato que
  escribe el usuario: ningún valor puede alterar la consulta a la base.

La base de datos es un archivo. No usar `":memory:"`: cada request HTTP abre su
propia conexión.

---

## 6. API HTTP — `api.py`

```python
crear_servidor(ruta_db: str, puerto: int = 0) -> ThreadingHTTPServer
```

### Contrato

**`POST /api/v1/reservas`**

```json
{
  "email": "ana@mail.com",
  "entrega": "MOTO",
  "entradas": [{"tipo": "VIP", "sector": "PALCO", "cantidad": 1}],
  "codigo": "PROMO2026",
  "fecha": "2026-10-01"
}
```

`codigo` y `fecha` son opcionales. La fecha viaja como texto en formato
`AAAA-MM-DD`. Respuesta exitosa:

```
201 Created
{"id": 1, "subtotal": "32500.50", "descuento": "8125.13", "cargo": "2000.00", "total": "26375.37"}
```

**`GET /api/v1/reservas/{id}`**

```
200 OK
```

Devuelve la reserva completa con el formato de `obtener_reserva`.

En las respuestas, **los montos viajan como texto** con dos decimales, nunca
como número.

### R11 — Errores

Todos los errores tienen este formato:

```json
{"error": {"code": "SECTOR_INVALIDO", "message": "Sector inválido: 'BALCON'"}}
```

| Situación | Status | `code` |
|---|---:|---|
| Un error de negocio de `entradas.py` | 422 | El de la sección 4 |
| El cuerpo no es JSON válido | 400 | `JSON_INVALIDO` |
| Falta `email`, `entrega` o `entradas`, o no son del tipo esperado | 400 | `DATOS_INCOMPLETOS` |
| La fecha no tiene formato `AAAA-MM-DD` | 400 | `FECHA_INVALIDA` |
| La reserva no existe | 404 | `RESERVA_INEXISTENTE` |
| Cualquier otra ruta | 404 | `RUTA_INEXISTENTE` |

Un error nunca puede devolver 500.
