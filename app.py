import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
import time

app = Flask(__name__)
CORS(app)

# Estado global del juego
grid = [[0 for _ in range(3)] for _ in range(3)]
juego_activo = True
jugadores = {}  # id_usuario -> jugador_numero (1 o 2)
turno_actual = 1
ultimo_movimiento = time.time()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/unirse", methods=["POST"])
def unirse():
    global jugadores
    # Elimina jugadores inactivos (>5min)
    ahora = time.time()
    jugadores = {uid: (num, t) for uid, (num, t) in jugadores.items() if ahora - t < 300}

    if len(jugadores) >= 2:
        return jsonify({"error": "Sala llena"}), 403

    uid = str(uuid.uuid4())
    numero = 1 if 1 not in [j[0] for j in jugadores.values()] else 2
    jugadores[uid] = (numero, ahora)
    return jsonify({"uid": uid, "jugador": numero})

@app.route("/estado", methods=["POST"])
def estado():
    data = request.get_json()
    uid = data.get("uid")
    if uid not in jugadores:
        return jsonify({"error": "Jugador no válido"}), 403

    # Actualiza último acceso
    jugadores[uid] = (jugadores[uid][0], time.time())
    return jsonify({
        "grid": grid,
        "activo": juego_activo,
        "turno": turno_actual,
        "soy": jugadores[uid][0]
    })

@app.route("/jugar", methods=["POST"])
def jugar():
    global grid, juego_activo, turno_actual, ultimo_movimiento
    data = request.get_json()
    uid = data.get("uid")
    pos = data.get("pos")

    if not juego_activo:
        return jsonify({"error": "Juego terminado."}), 400
    if uid not in jugadores:
        return jsonify({"error": "Jugador no válido"}), 403
    jugador = jugadores[uid][0]
    if jugador != turno_actual:
        return jsonify({"error": "No es tu turno"}), 403

    row, col = pos // 3, pos % 3
    actual = grid[row][col]

    # Reglas: 0→1, 1→2, 2→3
    if actual == 3 or (actual != jugador and actual != 0):
        return jsonify({"error": "Movimiento inválido"}), 400

    grid[row][col] = actual + 1

    if check_ganador():
        juego_activo = False
        return jsonify({"victoria": True})

    turno_actual = 1 if turno_actual == 2 else 2
    ultimo_movimiento = time.time()
    return jsonify({"ok": True})

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    global grid, juego_activo, turno_actual
    grid = [[0 for _ in range(3)] for _ in range(3)]
    juego_activo = True
    turno_actual = 1
    return jsonify({"ok": True})

def check_ganador():
    for i in range(3):
        if grid[i][0] != 0 and grid[i][0] == grid[i][1] == grid[i][2]: return True
        if grid[0][i] != 0 and grid[0][i] == grid[1][i] == grid[2][i]: return True
    if grid[0][0] != 0 and grid[0][0] == grid[1][1] == grid[2][2]: return True
    if grid[0][2] != 0 and grid[0][2] == grid[1][1] == grid[2][0]: return True
    return False

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
