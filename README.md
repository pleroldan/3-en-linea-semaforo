# 3-en-linea-semaforo
Desarrollo de el juego 3 en linea en su variante de semaforo


# 🟢🔶🔴 Reglamento Oficial – Ta-Te-Ti Semáforo
## 🎯 Objetivo del juego
Formar una línea continua de tres fichas del mismo color (verde, amarillo o rojo) en el tablero de 3×3, ya sea horizontal, vertical o diagonal.

## 👥 Jugadores
El juego se juega entre 2 jugadores.

No hay colores asignados a cada jugador. Ambos pueden colocar o transformar fichas dentro del ciclo permitido (verde → amarillo → rojo).

## 🧩 Componentes
Tablero de 3 filas por 3 columnas (3x3).

Cada casilla puede contener una ficha con color verde, amarillo o rojo, o estar vacía.

## 🔄 Turnos
En cada turno, un jugador debe realizar una única acción, eligiendo una casilla válida:

Colocar una ficha verde en una casilla vacía.

o

Reemplazar una ficha existente siguiendo el ciclo de colores:

Verde → Amarillo

Amarillo → Rojo

Rojo no puede ser reemplazada (es el nivel final).

## 🚫 Restricciones
No se puede colocar ficha en una casilla que ya contiene verde, amarillo o rojo.

No se puede reemplazar una ficha roja.

Solo se permite una acción por turno (colocar o reemplazar, nunca ambas).

## ✅ Condición de victoria
El juego termina inmediatamente cuando un jugador logra formar una línea de tres fichas del mismo color (verde, amarillo o rojo), ya sea:

En fila horizontal

En columna vertical

En diagonal

## 🤝 Empate
Si el tablero se llena sin que se forme una línea de tres colores iguales, se declara empate.



# 🚀  Estructura del proyecto



proyecto/  
├── app.py  
├── requirements.txt
├── static/  
│   └── style.css  
└── templates/
    └── index.html  
