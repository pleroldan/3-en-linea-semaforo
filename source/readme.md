# 🟢🔶🔴 Ta-Te-Ti Semáforo – Lógica del Juego

## 🎯 Objetivo
Ser el primer jugador en formar una línea de **tres fichas del mismo color** (verde, amarillo o rojo) en un tablero de 3x3. Las líneas válidas son:

- Horizontales
- Verticales
- Diagonales

---

## 🧩 Representación del Tablero

El tablero es una matriz de 3x3, donde cada celda tiene un valor que representa el color actual:

| Valor | Estado     |
|-------|------------|
| 0     | Vacía      |
| 1     | Verde      |
| 2     | Amarilla   |
| 3     | Roja       |

```python
tablero = [
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0]
]
```

---

## 🔄 Turnos de los Jugadores

En cada turno, el jugador puede realizar **una única acción**:

### 1. Colocar una ficha verde
- Solo en una casilla vacía (`== 0`).
```python
si tablero[fila][columna] == 0:
    tablero[fila][columna] = 1  # Verde
```

### 2. Reemplazar una ficha existente
- Verde → Amarillo → Rojo (no se puede reemplazar rojo).
```python
si tablero[fila][columna] == 1:
    tablero[fila][columna] = 2  # Verde → Amarillo
si tablero[fila][columna] == 2:
    tablero[fila][columna] = 3  # Amarillo → Rojo
si tablero[fila][columna] == 3:
    acción inválida
```

---

## ✅ Validación de Acción

Antes de aplicar cualquier acción, verificar:

```python
si acción == "colocar verde":
    permitir solo si celda está vacía (== 0)

si acción == "reemplazar":
    permitir solo si celda es verde (1) o amarilla (2)

si celda == 3:
    no se permite reemplazo
```

---

## 🏁 Condición de Victoria

Después de cada turno, verificar si hay 3 fichas del mismo color (`≠ 0`) en:

### A. Filas
```python
para cada fila:
    si fila == [x, x, x] y x ≠ 0:
        victoria
```

### B. Columnas
```python
para cada columna:
    si columna == [x, x, x] y x ≠ 0:
        victoria
```

### C. Diagonales
```python
si tablero[0][0] == tablero[1][1] == tablero[2][2] ≠ 0:
    victoria
si tablero[0][2] == tablero[1][1] == tablero[2][0] ≠ 0:
    victoria
```

---

## 🤝 Empate

El juego puede terminar en empate si:

- Todas las celdas están ocupadas (`≠ 0`)
- Y no se ha formado ninguna línea ganadora

```python
si todas las celdas ≠ 0 y no hay 3 en línea:
    empate
```

---

## 🔁 Flujo del Juego

```python
mientras no haya victoria ni empate:
    mostrar tablero
    pedir acción al jugador actual
    validar y aplicar acción
    verificar victoria
    cambiar de turno
```

---

## 🧠 Nota

- Ambos jugadores pueden interactuar con cualquier ficha del tablero (excepto las rojas).
- El color no pertenece a un jugador: la estrategia está en decidir **dónde poner** o **cuándo transformar** una ficha.
