import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "clave_secreta_unica"
CORS(app)

# Estado global del juego
grid = [[0 for _ in range(3)] for _ in range(3)]
juego_activo = True
jugadores = []

@app.route("/")
def index():
    if "jugador_id" not in session:
        jugador_id = str(uuid4())
        if len(jugadores) < 2:
            jugadores.append(jugador_id)
            session["jugador_id"] = jugador_id
        else:
            session["jugador_id"] = "espectador"
    return render_template("index.html")

@app.route("/estado")
def estado():
    jugador_id = session.get("jugador_id")
    turno = jugadores[0] if len(jugadores) == 2 and sum(cell != 0 for row in grid for cell in row) % 2 == 0 else jugadores[1]
    jugador_num = jugadores.index(jugador_id) + 1 if jugador_id in jugadores else 0
    return jsonify({
        "grid": grid,
        "activo": juego_activo,
        "jugador": jugador_num,
        "turno": jugadores.index(turno) + 1 if turno in jugadores else 0
    })

@app.route("/jugar", methods=["POST"])
def jugar():
    global grid, juego_activo

    if not juego_activo:
        return jsonify({"error": "Juego terminado."}), 400

    jugador_id = session.get("jugador_id")
    if jugador_id not in jugadores:
        return jsonify({"error": "No autorizado."}), 403

    turno = jugadores[0] if sum(cell != 0 for row in grid for cell in row) % 2 == 0 else jugadores[1]
    if jugador_id != turno:
        return jsonify({"error": "No es tu turno."}), 400

    data = request.get_json()
    pos = data.get("pos")

    row, col = pos // 3, pos % 3
    actual = grid[row][col]

    if actual == 0:
        grid[row][col] = 1  # Verde
    elif actual == 1:
        grid[row][col] = 2  # Amarillo
    elif actual == 2:
        grid[row][col] = 3  # Rojo
    else:
        return jsonify({"error": "No se puede reemplazar más."}), 400

    if check_ganador():
        juego_activo = False
        return jsonify({"victoria": True})
    return jsonify({"ok": True})

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    global grid, juego_activo, jugadores
    grid = [[0 for _ in range(3)] for _ in range(3)]
    juego_activo = True
    jugadores = []
    session.pop("jugador_id", None)
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
