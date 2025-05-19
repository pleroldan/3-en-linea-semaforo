import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Estado global del juego
grid = [[0 for _ in range(3)] for _ in range(3)]
juego_activo = True
turno = 1  # 1: jugador 1, 2: jugador 2

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estado")
def estado():
    return jsonify({
        "grid": grid,
        "activo": juego_activo,
        "turno": turno
    })

@app.route("/jugar", methods=["POST"])
def jugar():
    global grid, juego_activo, turno

    if not juego_activo:
        return jsonify({"error": "Juego terminado. Reinicie."}), 400

    data = request.get_json()
    pos = data.get("pos")  # 0 a 8
    row, col = pos // 3, pos % 3
    valor_actual = grid[row][col]

    if valor_actual == 0:
        grid[row][col] = 1  # verde
    elif valor_actual == 1:
        grid[row][col] = 2  # amarillo
    elif valor_actual == 2:
        grid[row][col] = 3  # rojo
    else:
        return jsonify({"error": "Casilla completa."}), 400

    if check_ganador():
        juego_activo = False
        return jsonify({"victoria": True})

    # Alternar turno
    turno = 2 if turno == 1 else 1

    return jsonify({"ok": True})

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    global grid, juego_activo, turno
    grid = [[0 for _ in range(3)] for _ in range(3)]
    juego_activo = True
    turno = 1
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
