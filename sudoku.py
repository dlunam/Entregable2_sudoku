import numpy as np
import random

# Crea una matriz 9x9 vacía
def crear_tablero():
    return np.zeros((9, 9), dtype=int)

# Verifica si se puede colocar el número en fila, columna y subcuadro 3x3
def es_valido(tablero, fila, col, num):
    if num in tablero[fila]:
        return False
    if num in tablero[:, col]:
        return False
    f_inicio = (fila // 3) * 3
    c_inicio = (col // 3) * 3
    if num in tablero[f_inicio:f_inicio+3, c_inicio:c_inicio+3]:
        return False
    return True

# Rellena completamente el tablero con una solución válida
def rellenar_sudoku(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if rellenar_sudoku(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

# Resuelve un sudoku incompleto por backtracking
def resolver_sudoku(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

# Crea un tablero con huecos para resolver
def generar_sudoku(casillas_vacias=40):
    tablero = crear_tablero()
    rellenar_sudoku(tablero)
    tablero_resuelto = tablero.copy()
    
    vaciados = 0
    while vaciados < casillas_vacias:
        fila = random.randint(0, 8)
        col = random.randint(0, 8)
        if tablero[fila][col] != 0:
            tablero[fila][col] = 0
            vaciados += 1
    return tablero, tablero_resuelto

# Imprime el tablero con formato visual
def imprimir_tablero(tablero):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(tablero[i][j] if tablero[i][j] != 0 else ".", end=" ")
        print()

# ------------------------
# Uso del programa
# ------------------------

# Generar Sudoku con 40 casillas vacías
sudoku_incompleto, solucion_real = generar_sudoku(casillas_vacias=40)

print("Sudoku para resolver:")
imprimir_tablero(sudoku_incompleto)

# Resolver el Sudoku por backtracking
resolver_sudoku(sudoku_incompleto)

print("\nSudoku resuelto:")
imprimir_tablero(sudoku_incompleto)
