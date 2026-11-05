import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import reservas

RUTA_RESERVAS = "/api/v1/reservas"
RUTA_RESERVA = re.compile(r"/api/v1/reservas/(\d+)")


class _Manejador(BaseHTTPRequestHandler):
    ruta_db = None

    def log_message(self, *args):
        pass

    def _responder(self, status, cuerpo):
        datos = json.dumps(cuerpo, default=float).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        if self.path != RUTA_RESERVAS:
            return self._responder(404, {"error": {"code": "RUTA_INEXISTENTE", "message": "La ruta no existe"}})
        try:
            largo = int(self.headers.get("Content-Length", 0))
            datos = json.loads(self.rfile.read(largo))
            con = reservas.conectar(self.ruta_db)
            reserva_id = reservas.guardar_reserva(
                con, datos["email"], datos["entradas"], datos["entrega"], datos.get("codigo"), datos.get("fecha")
            )
            reserva = reservas.obtener_reserva(con, reserva_id)
            con.close()
        except Exception as e:
            return self._responder(500, {"error": str(e)})
        resumen = {k: reserva[k] for k in ("id", "subtotal", "descuento", "cargo", "total")}
        self._responder(201, resumen)

    def do_GET(self):
        coincide = RUTA_RESERVA.fullmatch(self.path)
        if not coincide:
            return self._responder(404, {"error": {"code": "RUTA_INEXISTENTE", "message": "La ruta no existe"}})
        con = reservas.conectar(self.ruta_db)
        reserva = reservas.obtener_reserva(con, int(coincide.group(1)))
        con.close()
        self._responder(200, reserva)


def crear_servidor(ruta_db, puerto=0):
    con = reservas.conectar(ruta_db)
    reservas.crear_esquema(con)
    con.close()
    manejador = type("Manejador", (_Manejador,), {"ruta_db": ruta_db})
    return ThreadingHTTPServer(("127.0.0.1", puerto), manejador)


if __name__ == "__main__":
    servidor = crear_servidor("entradas.db", 8000)
    print("Escuchando en http://127.0.0.1:8000")
    servidor.serve_forever()
