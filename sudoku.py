import numpy as np

# Crear una matriz 9x9 inicializada en ceros
tablero = np.zeros((9, 9), dtype=int)

# Función para imprimir el tablero con formato Sudoku
def imprimir_tablero(tablero):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(tablero[i][j], end=" ")
        print()

# Ejemplo de uso
imprimir_tablero(tablero)
