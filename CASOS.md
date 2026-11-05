# **Casos de prueba de caja negra — Entradas para la fiesta de egresados**

**Base de pruebas:** exclusivamente ESPECIFICACION.md.

**Criterio:** se prueban las funciones según su contrato, sin asumir detalles de implementación.

---

## **R1 — Tipos de entrada**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Válida: GENERAL | Precio \$18.999,90 | {"tipo":"GENERAL","sector":"PISTA","cantidad":1} | Subtotal Decimal("18999.90") |
| Válida: VIP | Precio \$32.500,50 | {"tipo":"VIP","sector":"PISTA","cantidad":1} | Subtotal Decimal("32500.50") |
| Válida: ESTUDIANTE | Precio \$12.999,50 | {"tipo":"ESTUDIANTE","sector":"PISTA","cantidad":1} | Subtotal Decimal("12999.50") |
| Válida: minúsculas | Sin distinción de mayúsculas | {"tipo":"vip","sector":"PISTA","cantidad":1} | Subtotal Decimal("32500.50") |
| Válida: espacios | Espacios alrededor | {"tipo":" VIP ","sector":"PISTA","cantidad":1} | Subtotal Decimal("32500.50") |
| Inválida: tipo inexistente | Cualquier otro texto | {"tipo":"PREMIUM","sector":"PISTA","cantidad":1} | EntradaError, código TIPO\_INEXISTENTE |
| Inválida: tipo vacío | Texto vacío | {"tipo":"","sector":"PISTA","cantidad":1} | EntradaError, código TIPO\_INEXISTENTE |
| Inválida: tipo nulo | None | {"tipo":None,"sector":"PISTA","cantidad":1} | EntradaError, código TIPO\_INEXISTENTE |
| Ignorar precio externo | Precio enviado diferente | {"tipo":"VIP","sector":"PISTA","cantidad":1,"precio":1} | Subtotal Decimal("32500.50") |

## **R2 — Sectores**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Válida: PISTA | Sector permitido | {"tipo":"VIP","sector":"PISTA","cantidad":1} | Sin error |
| Válida: PLATEA | Sector permitido | {"tipo":"VIP","sector":"PLATEA","cantidad":1} | Sin error |
| Válida: PALCO | Sector permitido | {"tipo":"VIP","sector":"PALCO","cantidad":1} | Sin error |
| Válida: minúsculas | Sin distinción de mayúsculas | {"tipo":"VIP","sector":"palco","cantidad":1} | Sin error |
| Válida: espacios | Espacios alrededor | {"tipo":"VIP","sector":" PLATEA ","cantidad":1} | Sin error |
| Inválida: sector inexistente | Cualquier otro sector | {"tipo":"VIP","sector":"BALCON","cantidad":1} | EntradaError, código SECTOR\_INVALIDO |
| Inválida: vacío | Texto vacío | {"tipo":"VIP","sector":"","cantidad":1} | EntradaError, código SECTOR\_INVALIDO |
| Inválida: nulo | None | {"tipo":"VIP","sector":None,"cantidad":1} | EntradaError, código SECTOR\_INVALIDO |

## **R3 — Cantidad**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Válida: mínimo | 1 | {"tipo":"VIP","sector":"PISTA","cantidad":1} | Sin error |
| Válida: máximo | 8 | {"tipo":"VIP","sector":"PISTA","cantidad":8} | Sin error |
| Válida: intermedia | 4 | {"tipo":"VIP","sector":"PISTA","cantidad":4} | Sin error |
| Inválida: cero | 0 | {"tipo":"VIP","sector":"PISTA","cantidad":0} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: negativo | \-1 | {"tipo":"VIP","sector":"PISTA","cantidad":-1} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: supera máximo | 9 | {"tipo":"VIP","sector":"PISTA","cantidad":9} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: decimal | 1.5 | {"tipo":"VIP","sector":"PISTA","cantidad":1.5} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: booleano True | True | {"tipo":"VIP","sector":"PISTA","cantidad":true} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: booleano False | False | {"tipo":"VIP","sector":"PISTA","cantidad":false} | EntradaError, código CANTIDAD\_INVALIDA |
| Inválida: texto | "2" | {"tipo":"VIP","sector":"PISTA","cantidad":"2"} | EntradaError, código CANTIDAD\_INVALIDA |

## **R4 — Lista de entradas**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Válida: una entrada | Mínimo 1 elemento | \[{"tipo":"VIP","sector":"PALCO","cantidad":1}\] | Subtotal Decimal("32500.50") |
| Válida: varias entradas | Más de un elemento | \[{"tipo":"VIP","sector":"PALCO","cantidad":1},{"tipo":"GENERAL","sector":"PISTA","cantidad":2}\] | Subtotal Decimal("70499.70") |
| Inválida: lista vacía | 0 elementos | \[\] | EntradaError, código LISTA\_VACIA |
| Inmutabilidad de lista | Lista con una entrada | Ejecutar calcular\_subtotal(entradas) y comparar antes y después | La lista permanece idéntica |
| Inmutabilidad de entrada | Diccionario con claves adicionales | Ejecutar validar\_entrada(entrada) y comparar antes y después | El diccionario permanece idéntico |
| Inmutabilidad de varias entradas | Lista con varias entradas | Ejecutar calcular\_total(entradas, "MOTO") y comparar antes y después | Lista y diccionarios permanecen idénticos |

## **R5 — Descuento por grupo**

Se utiliza una entrada GENERAL de \$18.999,90 para facilitar el cálculo.

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Sin descuento | 1 entrada | Subtotal 18999.90, cantidad 1 | Descuento Decimal("0.00") |
| Sin descuento | 5 entradas | Subtotal 94999.50, cantidad 5 | Descuento Decimal("0.00") |
| Con descuento | 6 entradas | Subtotal 113999.40, cantidad 6 | Descuento Decimal("13679.93") |
| Con descuento | Más de 6 entradas | Subtotal 132999.30, cantidad 7 | Descuento Decimal("15959.92") |
| Suma de cantidades | Dos líneas de 3 entradas | Subtotal 113999.40, cantidad total 6 | Descuento Decimal("13679.93") |

## **R6 — Códigos promocionales**

Fecha de referencia: 2026-12-15.

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Sin código: None | Sin código | Subtotal 50000.00, cantidad 1, código None | Descuento Decimal("0.00") |
| Sin código: vacío | Texto vacío | Subtotal 50000.00, cantidad 1, código "" | Descuento Decimal("0.00") |
| Sin código: espacios | Solo espacios | Subtotal 50000.00, cantidad 1, código " " | Descuento Decimal("0.00") |
| PROMO2026 válido | Antes del vencimiento | Subtotal 100000.00, código "PROMO2026", fecha 2026-12-14 | Descuento Decimal("25000.00") |
| PROMO2026 válido | Último día inclusive | Subtotal 100000.00, código "PROMO2026", fecha 2026-12-15 | Descuento Decimal("25000.00") |
| PROMO2026 vencido | Día siguiente | Subtotal 100000.00, código "PROMO2026", fecha 2026-12-16 | EntradaError, código CODIGO\_VENCIDO |
| PROMO2026 normalizado | Minúsculas y espacios | Subtotal 100000.00, código " promo2026 ", fecha 2026-10-01 | Descuento Decimal("25000.00") |
| AMIGO válido | Subtotal igual al mínimo | Subtotal 40000.00, código "AMIGO" | Descuento Decimal("5000.00") |
| AMIGO válido | Subtotal superior al mínimo | Subtotal 50000.00, código "AMIGO" | Descuento Decimal("5000.00") |
| AMIGO inválido | Subtotal inferior al mínimo | Subtotal 39999.99, código "AMIGO" | EntradaError, código CODIGO\_MINIMO\_NO\_ALCANZADO |
| AMIGO normalizado | Minúsculas y espacios | Subtotal 50000.00, código " amigo " | Descuento Decimal("5000.00") |
| Código inexistente | Código desconocido | Subtotal 50000.00, código "OTRO2026" | EntradaError, código CODIGO\_INVALIDO |
| Mayor descuento: grupo | Grupo supera código AMIGO | Subtotal 120000.00, cantidad 6, código "AMIGO" | Descuento Decimal("14400.00") |
| Mayor descuento: código | PROMO supera grupo | Subtotal 120000.00, cantidad 6, código "PROMO2026", fecha 2026-10-01 | Descuento Decimal("30000.00") |
| Descuento no supera subtotal | Código promocional | Subtotal 100.00, cantidad 1, código "PROMO2026", fecha 2026-10-01 | Descuento Decimal("25.00") |
| Fecha omitida | Fecha actual de la llamada | Subtotal 50000.00, código "PROMO2026", fecha None | Descuento según la fecha real de ejecución: 12500.00 si no venció; CODIGO\_VENCIDO si venció |

## **R7 — Dinero y redondeo**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Importe con dos decimales | Precio GENERAL | calcular\_subtotal(\[{"tipo":"GENERAL","sector":"PISTA","cantidad":1}\]) | Decimal("18999.90") |
| Medio centavo hacia arriba | 25 % de 32500.50 | Subtotal Decimal("32500.50"), código PROMO2026 | Decimal("8125.13") |
| Redondeo de grupo | 12 % de 113999.40 | Subtotal Decimal("113999.40"), cantidad 6 | Decimal("13679.93") |
| Cargo entero | Cargo MOTO | Base Decimal("10000.00"), entrega "MOTO" | Decimal("2000.00") |
| Todos los importes Decimal | Compra VIP con MOTO y PROMO2026 | Calcular total según ejemplo R9 | Los cuatro valores son instancias de Decimal y tienen dos decimales |

## **R8 — Cargo por entrega**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| RETIRO válido | Cargo cero | Base Decimal("10000.00"), entrega "RETIRO" | Decimal("0.00") |
| MOTO válido | Cargo \$2.000 | Base Decimal("10000.00"), entrega "MOTO" | Decimal("2000.00") |
| CORREO válido | Cargo \$3.500 | Base Decimal("10000.00"), entrega "CORREO" | Decimal("3500.00") |
| Normalización | Minúsculas y espacios | Base Decimal("10000.00"), entrega " moto " | Decimal("2000.00") |
| Inválida | Entrega desconocida | Base Decimal("10000.00"), entrega "DELIVERY" | EntradaError, código ENTREGA\_INVALIDA |
| Inválida | Texto vacío | Base Decimal("10000.00"), entrega "" | EntradaError, código ENTREGA\_INVALIDA |
| Cargo gratis | Base inferior al límite | Base Decimal("79999.99"), entrega "MOTO" | Decimal("2000.00") |
| Cargo gratis | Base exactamente en el límite | Base Decimal("80000.00"), entrega "MOTO" | Decimal("0.00") |
| Cargo gratis | Base superior al límite | Base Decimal("80000.01"), entrega "CORREO" | Decimal("0.00") |

## **R9 — Total**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Compra sin descuento ni cargo | GENERAL, RETIRO | \[{"tipo":"GENERAL","sector":"PISTA","cantidad":1}\], entrega "RETIRO" | {"subtotal": Decimal("18999.90"), "descuento": Decimal("0.00"), "cargo": Decimal("0.00"), "total": Decimal("18999.90")} |
| Compra con cargo | GENERAL, MOTO | \[{"tipo":"GENERAL","sector":"PISTA","cantidad":1}\], entrega "MOTO" | {"subtotal": Decimal("18999.90"), "descuento": Decimal("0.00"), "cargo": Decimal("2000.00"), "total": Decimal("20999.90")} |
| Compra con descuento y cargo | Ejemplo de especificación | \[{"tipo":"VIP","sector":"PALCO","cantidad":1}\], entrega "MOTO", código "PROMO2026", fecha 2026-10-01 | {"subtotal": Decimal("32500.50"), "descuento": Decimal("8125.13"), "cargo": Decimal("2000.00"), "total": Decimal("26375.37")} |
| Compra con cargo gratis | Base igual a \$80.000 | Compra cuya base sea 80000.00, entrega "MOTO" | Cargo Decimal("0.00"); total igual a subtotal menos descuento |
| Total con varias líneas | Dos entradas diferentes | VIP x1 y GENERAL x1, entrega RETIRO | Subtotal Decimal("51500.40"), descuento Decimal("0.00"), cargo Decimal("0.00"), total Decimal("51500.40") |

## **Orden de validación — calcular\_total**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Lista vacía y entrega inválida | Dos errores simultáneos | \[\], entrega "INVALIDA" | LISTA\_VACIA |
| Tipo y sector inválidos | Dos errores en la misma entrada | {"tipo":"OTRO","sector":"BALCON","cantidad":1} | TIPO\_INEXISTENTE |
| Sector y cantidad inválidos | Dos errores en la misma entrada | {"tipo":"VIP","sector":"BALCON","cantidad":0} | SECTOR\_INVALIDO |
| Cantidad y código inválidos | Dos errores simultáneos | Cantidad 0, código "DESCONOCIDO" | CANTIDAD\_INVALIDA |
| Entrada y código inválidos | Dos errores simultáneos | Tipo "OTRO", código "DESCONOCIDO" | TIPO\_INEXISTENTE |
| Código y entrega inválidos | Dos errores simultáneos | Entrada válida, código "DESCONOCIDO", entrega "INVALIDA" | CODIGO\_INVALIDO |
| Entrada posterior inválida | Dos entradas, primera válida y segunda inválida | Primera VIP válida, segunda con tipo "OTRO" | TIPO\_INEXISTENTE de la segunda entrada |
| Validación por orden de líneas | Dos entradas inválidas | Primera con sector inválido; segunda con tipo inválido | SECTOR\_INVALIDO |

## **R10 — Persistencia**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| Guardado correcto | Una entrada válida | Guardar VIP x1 con MOTO y PROMO2026 | Devuelve un ID entero |
| Error de negocio | Entrada inválida | Guardar una entrada con tipo "OTRO" | Propaga EntradaError con TIPO\_INEXISTENTE; no queda reserva ni detalle |
| Atomicidad | Error durante la operación | Guardar compra inválida y consultar la base | No existe reserva parcial ni entradas asociadas |
| Persistencia definitiva | Dos conexiones distintas | Guardar mediante conexión A y consultar mediante conexión B | La conexión B ve la reserva completa y todas sus entradas |
| Importes exactos | Compra del ejemplo R9 | Guardar VIP x1 con MOTO y PROMO2026 | Los cuatro importes vuelven como Decimal con valores idénticos |
| Precio confiable | Precio externo manipulado | Entrada VIP con "precio": 1 | precio\_unitario es Decimal("32500.50") |
| Normalización email | Mayúsculas y espacios | Email " Ana@Mail.com " | Se guarda "ana@mail.com" |
| Normalización entrega | Minúsculas y espacios | Entrega " moto " | Se guarda "MOTO" |
| Normalización código | Minúsculas y espacios | Código " promo2026 " | Se guarda "PROMO2026" |
| Código vacío | Texto vacío | Código "" | Se guarda None |
| Código con espacios | Solo espacios | Código " " | Se guarda None |
| Normalización entrada | Tipo y sector con espacios y minúsculas | Tipo " vip ", sector " palco " | Se guardan "VIP" y "PALCO" |
| ID inexistente | ID que no existe | obtener\_reserva(con, 999999\) | None |
| Consulta email normalizado | Email con espacios y mayúsculas | Guardar "ana@mail.com" y consultar " ANA@MAIL.COM " | Devuelve la reserva |
| Orden de reservas | Dos reservas del mismo email | Guardar una y luego otra | reservas\_de devuelve primero la más reciente |
| Seguridad de consulta | Email con caracteres SQL | Consultar con "x' OR 1=1 \--" | Se trata como dato literal; no altera la consulta |
| Orden de entradas | Varias líneas | Guardar VIP, GENERAL y ESTUDIANTE | obtener\_reserva devuelve las entradas en ese mismo orden |

## **R11 — API HTTP**

| Partición | Valores límite | Entrada | Resultado esperado |
| ----- | ----- | ----- | ----- |
| POST válido | Compra del ejemplo | POST /api/v1/reservas con JSON completo | HTTP 201; respuesta {"id":1,"subtotal":"32500.50","descuento":"8125.13","cargo":"2000.00","total":"26375.37"} |
| POST sin código | Código opcional omitido | JSON válido sin codigo | HTTP 201 si los demás datos son válidos |
| POST sin fecha | Fecha opcional omitida | JSON válido sin fecha | HTTP 201 si los demás datos son válidos |
| JSON inválido | Cuerpo que no es JSON | POST con cuerpo "{" | HTTP 400, código JSON\_INVALIDO |
| Falta email | Campo ausente | JSON sin email | HTTP 400, código DATOS\_INCOMPLETOS |
| Falta entrega | Campo ausente | JSON sin entrega | HTTP 400, código DATOS\_INCOMPLETOS |
| Falta entradas | Campo ausente | JSON sin entradas | HTTP 400, código DATOS\_INCOMPLETOS |
| Email tipo incorrecto | Email numérico | "email":123 | HTTP 400, código DATOS\_INCOMPLETOS |
| Entrega tipo incorrecto | Entrega numérica | "entrega":123 | HTTP 400, código DATOS\_INCOMPLETOS |
| Entradas tipo incorrecto | Entradas como texto | "entradas":"VIP" | HTTP 400, código DATOS\_INCOMPLETOS |
| Fecha formato incorrecto | AAAA/MM/DD | "fecha":"2026/10/01" | HTTP 400, código FECHA\_INVALIDA |
| Fecha formato incorrecto | Fecha incompleta | "fecha":"2026-10" | HTTP 400, código FECHA\_INVALIDA |
| Fecha inválida | Día inexistente | "fecha":"2026-02-30" | HTTP 400, código FECHA\_INVALIDA |
| Error de negocio | Sector inexistente | Entrada con sector "BALCON" | HTTP 422, código SECTOR\_INVALIDO |
| Error de negocio | Tipo inexistente | Entrada con tipo "PREMIUM" | HTTP 422, código TIPO\_INEXISTENTE |
| Error de negocio | Cantidad inválida | Cantidad 9 | HTTP 422, código CANTIDAD\_INVALIDA |
| Error de negocio | Código inválido | Código "DESCONOCIDO" | HTTP 422, código CODIGO\_INVALIDO |
| GET existente | ID guardado | GET /api/v1/reservas/1 | HTTP 200; devuelve la reserva completa |
| GET inexistente | ID desconocido | GET /api/v1/reservas/999999 | HTTP 404, código RESERVA\_INEXISTENTE |
| Ruta inexistente | Ruta no definida | GET /otra-ruta | HTTP 404, código RUTA\_INEXISTENTE |
| Formato monetario | Respuesta exitosa | Consultar reserva | Todos los importes son textos con exactamente dos decimales, nunca números |
| Formato de error | Cualquier error | Generar un error de negocio | JSON con estructura {"error":{"code":"...","message":"..."}} |
| Sin errores 500 | Cualquier entrada inválida | Enviar datos inválidos | Nunca responde HTTP 500 |

---

## **Observaciones generales**

* Todos los importes se comparan como Decimal, nunca como float.  
* Los errores se verifican por su atributo code.  
* Las pruebas de normalización deben comprobar tanto el resultado como los datos efectivamente almacenados.  
* Las pruebas de persistencia deben usar una base SQLite en archivo, no :memory:.  
* Las pruebas de API deben comprobar status HTTP y estructura JSON.  
* Las pruebas de orden de validación deben incluir más de un error simultáneo.  
* Los valores de frontera deben probarse tanto en el límite como inmediatamente antes y después cuando corresponda.  
* No se debe modificar ninguna entrada ni lista recibida por las funciones.

**Fin de los casos de prueba de caja negra.**

