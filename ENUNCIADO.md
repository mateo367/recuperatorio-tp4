# TP 4 — Recuperatorio: Entradas para la fiesta de egresados

Mateo Roza Malachane · Individual · 1 semana · Testing

## Entrega

Entregá el link a un repositorio nuevo con visibilidad publica: el historial de commits se
corrige. El repositorio tiene que tener estos archivos, con estos nombres
exactos:

| Archivo | Contenido |
|---|---|
| `entradas.py` | Tu versión corregida |
| `test_entradas.py` | Tus tests unitarios |
| `test_integracion.py` | Tus tests de integración |
| `test_e2e.py` | Tus tests end-to-end |
| `CASOS.md` | Parte 1 |
| `AUDITORIA.md` | Parte 2 |
| `REFLEXION.md` | Parte 5 |
| `cobertura.txt` | El reporte de cobertura de tu suite final |


## Rúbrica

| Parte | Criterio | Puntos |
|---|---|---:|
| 1 | Casos de caja negra | 10 |
| 2 | Auditoría de la suite de la IA y del código | 15 |
| 3 | `entradas.py` corregido | 10 |
| 3 | Mutación de la suite unitaria | 10 |
| 3 | Historial TDD, calidad y cobertura | 5 |
| 4 | Fallas detectadas por la suite de integración | 10 |
| 4 | Fallas detectadas por la suite E2E | 10 |
| 5 | Reflexión | 30 |
| | **Total** | **100** |

Para aprobar necesitás 60 puntos y aprobar un coloquio de diez minutos sobre
esta entrega.

## Situación

Una IA escribió el backend de la venta de entradas para la fiesta de
egresados. Son tres módulos de Python:

- `entradas.py` calcula el precio de una compra.
- `reservas.py` guarda las reservas en una base de datos.
- `api.py` recibe las reservas por HTTP.

La IA también escribió ocho tests para `entradas.py`. Los ocho pasan, pero
entre los tres módulos hay más de veinte fallas.

## Qué recibís

| Archivo | Para qué |
|---|---|
| `ESPECIFICACION.md` | Describe cómo tiene que funcionar el sistema. Si el código y la especificación no coinciden, el error está en el código. |
| `entradas.py` | Lo vas a corregir. |
| `reservas.py`, `api.py` | Les vas a escribir tests. No hace falta corregirlos. |
| `test_entradas_ia.py` | Los tests de la IA. Los vas a evaluar. |
| `test_entradas.py`, `test_integracion.py`, `test_e2e.py` | Plantillas para tus tests. |
| `mutar.py` | Herramienta para medir tu suite unitaria. |
| `ruff.toml` | Configuración del linter. |

Para preparar el entorno, desde la carpeta del recuperatorio:

```bash
pip install pytest pytest-cov ruff
git init && git add . && git commit -m "Estado inicial"
```

## Cómo funciona el sistema

Una reserva pasa por los tres módulos:

1. El frontend manda la reserva a `api.py` por HTTP.
2. `api.py` se la pasa a `reservas.py`.
3. `reservas.py` le pide los importes a `entradas.py` y guarda la reserva en la
   base de datos.

La base de datos es SQLite, que **ya viene integrada en Python**. No hay que
instalar nada ni levantar un servidor de base de datos: toda la base es un
solo archivo, `entradas.db`, que se crea solo la primera vez que arranca la
API. El único servidor que se levanta es el de `api.py`.

Para probar el sistema a mano:

**1. Levantá la API.**

```bash
python api.py
```

Queda escuchando en `http://127.0.0.1:8000`. Para detenerla, Ctrl+C.

**2. Mandale reservas desde otra terminal.** Para consultar una reserva, abrí
en el navegador `http://127.0.0.1:8000/api/v1/reservas/1`. Para crear una,
guardá este script como `probar.py` y corrélo con `python probar.py`:

```python
import json, urllib.request

compra = {"email": "ana@mail.com", "entrega": "MOTO",
          "entradas": [{"tipo": "VIP", "sector": "PALCO", "cantidad": 1}]}
req = urllib.request.Request("http://127.0.0.1:8000/api/v1/reservas",
                             data=json.dumps(compra).encode(), method="POST")
with urllib.request.urlopen(req) as r:
    print(r.status, r.read().decode())
```

**3. Mirá qué quedó guardado en la base.**

```bash
python -c "import sqlite3; print(*sqlite3.connect('entradas.db').execute('SELECT * FROM reservas'), sep='\n')"
```

También podés abrir `entradas.db` con DB Browser for SQLite o con la extensión
SQLite Viewer de VS Code.

**4. Para empezar de cero**, detené la API y borrá `entradas.db`.

**Para correr los tests no hace falta nada de esto.** Las plantillas de
integración y E2E crean una base de datos nueva y vacía para cada test, y la
plantilla E2E levanta su propio servidor.

## Las plantillas de tests

Las tres plantillas ya traen escrito el código auxiliar que vas a necesitar y
**un test de ejemplo** cada una. Escribí tus tests debajo del ejemplo,
siguiendo el mismo estilo, y no borres el ejemplo. Para usar una fixture, poné
su nombre como parámetro del test.

**`test_entradas.py`** · ejemplo: `test_cantidad_cero_es_invalida`

| Nombre | Qué hace |
|---|---|
| `entrada(tipo, sector, cantidad)` | Arma una entrada. Sin argumentos, una GENERAL en PISTA. |
| `codigo_de_error(funcion, *args)` | Llama a la función con esos argumentos y devuelve el `code` del `EntradaError` que lanza. Si no lanza error, el test falla. |
| `HOY_VIGENTE` | Una fecha en la que `PROMO2026` todavía es válido. |

**`test_integracion.py`** · ejemplo: `test_un_id_inexistente_devuelve_none`

| Nombre | Qué hace |
|---|---|
| `con` (fixture) | Una conexión a una base nueva y vacía, distinta en cada test. |
| `ruta` (fixture) | La ruta del archivo de esa base. Sirve para abrir otra conexión con `reservas.conectar(ruta)`. |
| `contar(ruta, tabla)` | Cuenta las filas de la tabla `reservas` o `lineas`, desde una conexión nueva. |
| `entrada(...)`, `HOY_VIGENTE` | Iguales que en `test_entradas.py`. |

**`test_e2e.py`** · ejemplo: `test_una_ruta_inexistente_devuelve_404`

| Nombre | Qué hace |
|---|---|
| `url` (fixture) | Levanta el servidor con una base nueva y te da su dirección. Lo apaga cuando termina el test. |
| `pedir(url, metodo, ruta, cuerpo)` | Manda un request y devuelve `(status, cuerpo)`. Con `crudo=b"..."` en lugar de `cuerpo`, manda los bytes tal cual. |
| `compra(**cambios)` | Arma el cuerpo de una reserva válida. Con argumentos, cambia esos campos: `compra(entrega="CORREO")`. |
| `RUTA` | `"/api/v1/reservas"` |

## Reglas

1. No cambies los nombres ni los parámetros de las funciones, las rutas de la
   API ni `EntradaError`.
2. No modifiques `ESPECIFICACION.md`.
3. Tus tests tienen que comprobar lo que dice la especificación, no lo que
   hace el código.
4. Las fixtures van en el mismo archivo de tests. No uses `conftest.py`.
5. Todo lo que afirmes en `AUDITORIA.md` y en `REFLEXION.md` tiene que poder
   verificarse en tu repositorio. Si mencionás un test, tiene que existir con
   ese nombre. Si das una cifra, tiene que salir de una salida que pegaste.

## Consignas

### Parte 1 — Casos de caja negra · `CASOS.md`

Hacé esta parte **antes de leer el código**, trabajando solo con
`ESPECIFICACION.md`.

Para cada regla de R1 a R11, escribí:

- las particiones válidas e inválidas,
- los valores límite,
- al menos un caso por partición, con la entrada exacta y el resultado exacto
  que debería dar.

Podés usar una tabla por regla con estas columnas:

| Partición | Valores límite | Entrada | Resultado esperado |
|---|---|---|---|

Hacé un commit con `CASOS.md` antes del primer cambio a `entradas.py`. El orden
se revisa en el historial de git.

### Parte 2 — Auditoría · `AUDITORIA.md`

El archivo tiene dos secciones.

**Sección 1: los tests de la IA**

1. Para cada uno de los ocho tests de `test_entradas_ia.py`, indicá si es útil,
   débil, tautológico o inútil, y explicá por qué en una línea.
2. Corré `python mutar.py --tests test_entradas_ia.py` y anotá el puntaje.
3. Esta suite cubre más del 80% del código y no detecta ninguna falla.
   Explicá por qué.

**Sección 2: hallazgos**

1. Corré `ruff check entradas.py`.
2. Leé `entradas.py`, `reservas.py` y `api.py`.
3. Por cada falla que encuentres, anotá:
   - archivo y línea,
   - categoría,
   - regla de la especificación que no cumple,
   - cómo la encontraste,
   - severidad: alta, media o baja.
4. Terminá con una tabla de todas las fallas, de la más grave a la menos
   grave.

Categorías: lógica y límites · numéricos · strings · efectos laterales ·
fechas · seguridad · manejo de errores · tipos · code smell.

Las fallas de `reservas.py` y `api.py` se documentan acá, pero no se corrigen.

### Parte 3 — `entradas.py` y sus tests unitarios · `test_entradas.py`

**Corrección con TDD.** Por cada falla que corrijas:

1. Escribí un test que la demuestre y corrélo: tiene que fallar. Hacé un
   commit.
2. Corregí `entradas.py` y volvé a correr el test: tiene que pasar. Hacé otro
   commit.

```bash
git commit -m "test(R2): <comportamiento esperado>"
git commit -m "fix(R2): <qué corregiste>"
```

No hace falta corregir todas las fallas. Tiene que haber al menos 5 pares de
commits como estos.

**La suite.** Todos tus tests unitarios van en `test_entradas.py`. Cuando
termines, la suite tiene que:

- pasar completa contra tu `entradas.py` corregido,
- tener cobertura de ramas de 85% o más,
- tener un puntaje de mutación de 85% o más,
- seguir el patrón Arrange-Act-Assert,
- tener nombres que digan qué comportamiento prueba cada test,
- no tener asserts débiles: nada de `is not None`, `> 0` ni tests sin assert.

Generá `cobertura.txt` **al final**, con la suite completa y en verde, parado
en la carpeta donde están `entradas.py` y los tests:

```bash
pytest test_entradas.py --cov=entradas --cov-branch --cov-report=term-missing > cobertura.txt
python mutar.py
```

### Parte 4 — Integración y end-to-end · `test_integracion.py`, `test_e2e.py`

En esta parte **no corregís** `reservas.py` ni `api.py`: solo les escribís
tests.

**Integración.** En `test_integracion.py`, probá `reservas.py` contra una base
SQLite real. Elegí 4 puntos de R10 y escribí al menos un test por cada uno. No
uses mocks.

**End-to-end.** En `test_e2e.py`, levantá el servidor y mandale requests HTTP
reales. Escribí al menos un test por cada endpoint (`POST` y `GET`) y por cada
uno de 4 errores de la tabla de R11.

**Qué esperar.** Contra el `reservas.py` y el `api.py` que recibiste, varios de
tus tests van a fallar: esas son las fallas que estás buscando. Un test que
falla contra este código está bien. Un test que fallaría aunque el código
cumpliera la especificación está mal escrito.

**Antes de entregar,** corré `pytest --collect-only -q`. Si algún archivo de
tests muestra `0 items`, no tiene tests que corregir.

### Parte 5 — Reflexión · `REFLEXION.md`

Respondé las seis preguntas. Cada una vale 5 puntos. En cada respuesta:

- escribí entre cuatro y ocho oraciones,
- citá al menos una evidencia de tu repositorio: el nombre de un test, una
  salida que pegaste o un commit.

Una respuesta correcta pero general, que se podría escribir sin haber hecho el
recuperatorio, no obtiene el puntaje completo.

1. ¿Cuántos tests unitarios, de integración y E2E tenés? Pegá la salida de
   `pytest --collect-only -q`. ¿Por qué esa proporción?
2. ¿Qué falla de `reservas.py` no podía encontrarse con un test unitario de
   `entradas.py`? ¿Por qué?
3. ¿Qué falla de `api.py` estaba en el paso de información entre dos partes del
   sistema? ¿Qué parte tendría que haberla resuelto?
4. ¿Qué falla de `entradas.py` quedaba oculta detrás de otra, y recién apareció
   cuando corregiste la primera? ¿Qué test la detectó?
5. ¿Qué mide la cobertura, qué mide la mutación y qué mide la inyección de
   fallas? ¿En qué se diferencia un test que manda un dato inválido de una
   inyección de fallas?
6. ¿Cómo comprobaste, antes de entregar, que cada test, cifra y salida que
   citás en `AUDITORIA.md` y en esta reflexión corresponde a tu repositorio?

## Comandos útiles

| Para | Comando |
|---|---|
| Ver qué tests encuentra pytest | `pytest --collect-only -q` |
| Correr todos los tests | `pytest` |
| Correr un solo archivo | `pytest test_e2e.py` |
| Ver el nombre y el resultado de cada test | `pytest -v` |
| Generar el reporte de cobertura | `pytest test_entradas.py --cov=entradas --cov-branch --cov-report=term-missing > cobertura.txt` |
| Medir la mutación de tu suite | `python mutar.py` |
| Correr el linter | `ruff check entradas.py` |
| Levantar la API | `python api.py` |
| Ver tu historial de commits | `git log --oneline` |
