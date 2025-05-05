import os
import time
import random
import numpy as np
from time import perf_counter

# -------------------------------------------------------------------
# Utilidades de consola
# -------------------------------------------------------------------

def limpiar_consola():
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

# -------------------------------------------------------------------
# Generación y validación de tableros
# -------------------------------------------------------------------

def crear_tablero():
    """
    Crea y devuelve un tablero de Sudoku 9x9 vacío (todo ceros).
    """
    return np.zeros((9, 9), dtype=int)

def es_valido(tablero, fila, col, num):
    """
    Comprueba si colocar 'num' en la posición (fila, col) no viola
    las reglas de Sudoku (fila, columna y subcuadro 3x3).
    """
    # Reglas de fila y columna
    if num in tablero[fila] or num in tablero[:, col]:
        return False
    # Regla de subcuadro 3x3
    f0, c0 = (fila // 3) * 3, (col // 3) * 3
    if num in tablero[f0:f0+3, c0:c0+3]:
        return False
    return True

def rellenar_sudoku(tablero):
    """
    Rellena completamente el tablero con una solución válida usando
    backtracking aleatorio.
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if rellenar_sudoku(tablero):
                            return True
                        tablero[i][j] = 0
                return False
    return True

def generar_sudoku(casillas_vacias=40):
    """
    Genera un Sudoku completo y luego vacía 'casillas_vacias' posiciones
    al azar, devolviendo el tablero incompleto y su solución.
    """
    tablero = crear_tablero()
    rellenar_sudoku(tablero)
    solucion = tablero.copy()
    vaciados = 0
    while vaciados < casillas_vacias:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if tablero[i][j] != 0:
            tablero[i][j] = 0
            vaciados += 1
    return tablero, solucion

# -------------------------------------------------------------------
# Impresión de tablero
# -------------------------------------------------------------------

def imprimir_tablero(tablero):
    """
    Muestra el tablero en consola con separadores cada 3 filas/columnas.
    Las casillas vacías se representan con '.'.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            celda = tablero[i][j]
            print(celda if celda != 0 else ".", end=" ")
        print()

# -------------------------------------------------------------------
# Backtracking estándar
# -------------------------------------------------------------------

def resolver_sudoku(tablero):
    """
    Resuelve el Sudoku incompleto por backtracking sin heurísticas.
    Devuelve True si encuentra solución, y deja el tablero resuelto.
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[i][j] = 0  # backtrack
                return False  # no hay candidato válido
    return True  # tablero completo

# -------------------------------------------------------------------
# Heurística MRV (Minimum Remaining Value)
# -------------------------------------------------------------------

def celdas_vacias_con_opciones(tablero):
    """
    Devuelve lista de (fila, col, [opciones]) para cada celda vacía,
    ordenadas por menor número de opciones (MRV).
    """
    celdas = []
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                opciones = [n for n in range(1, 10) if es_valido(tablero, i, j, n)]
                celdas.append((i, j, opciones))
    celdas.sort(key=lambda x: len(x[2]))
    return celdas

def resolver_sudoku_mrv(tablero):
    """
    Resuelve el Sudoku usando backtracking + heurística MRV.
    """
    celdas = celdas_vacias_con_opciones(tablero)
    if not celdas:
        return True  # tablero completo
    i, j, opciones = celdas[0]
    for num in opciones:
        tablero[i][j] = num
        if resolver_sudoku_mrv(tablero):
            return True
        tablero[i][j] = 0  # backtrack
    return False

# -------------------------------------------------------------------
# Simulaciones paso a paso
# -------------------------------------------------------------------

def resolver_sudoku_simulado(tablero, delay=0.03):
    """
    Simula la resolución por backtracking estándar paso a paso.
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        limpiar_consola()
                        print("Simulación: Backtracking Estándar\n")
                        imprimir_tablero(tablero)
                        time.sleep(delay)
                        if resolver_sudoku_simulado(tablero, delay):
                            return True
                        tablero[i][j] = 0
                        limpiar_consola()
                        print("Retroceso Estándar...\n")
                        imprimir_tablero(tablero)
                        time.sleep(delay)
                return False
    return True

def resolver_sudoku_mrv_simulado(tablero, delay=0.03):
    """
    Simula la resolución usando heurística MRV paso a paso.
    """
    celdas = celdas_vacias_con_opciones(tablero)
    if not celdas:
        return True
    i, j, opciones = celdas[0]
    for num in opciones:
        tablero[i][j] = num
        limpiar_consola()
        print("Simulación: Heurística MRV\n")
        imprimir_tablero(tablero)
        time.sleep(delay)
        if resolver_sudoku_mrv_simulado(tablero, delay):
            return True
        tablero[i][j] = 0
        limpiar_consola()
        print("Retroceso MRV...\n")
        imprimir_tablero(tablero)
        time.sleep(delay)
    return False

# -------------------------------------------------------------------
# Programa principal
# -------------------------------------------------------------------

if __name__ == "__main__":
    # 1) Elegir número de casillas vacías
    while True:
        try:
            n_vacias = int(input("¿Cuántas casillas vacías quieres en el Sudoku (0–81)?: "))
            if 0 <= n_vacias <= 81:
                break
            print("Debe estar entre 0 y 81.")
        except ValueError:
            print("Introduce un número válido.")

    # 2) Generar y mostrar tablero para resolver
    sud, sol = generar_sudoku(casillas_vacias=n_vacias)
    print("\nSudoku para resolver:")
    imprimir_tablero(sud)

    # 3) Resolver y mostrar solución estándar
    tab_est = sud.copy()
    resolver_sudoku(tab_est)
    print("\nSolución (Backtracking Estándar):")
    imprimir_tablero(tab_est)

    # 4) Comparar tiempos de ambos métodos
    t1 = perf_counter()
    resolver_sudoku(sud.copy())
    t1 = perf_counter() - t1

    t2 = perf_counter()
    resolver_sudoku_mrv(sud.copy())

    t2 = perf_counter() - t2

    print(f"\nTiempo Estándar: {t1:.6f} s")
    print(f"Tiempo MRV:      {t2:.6f} s")

    # 5) Preguntar simulación
    print("\n¿Quieres ver simulación paso a paso?")
    print("1) Estándar\n2) MRV\n3) Ambos\nOtro) Ninguno")
    opción = input("Elige opción: ").strip()

    if opción in ('1', '3'):
        temp = sud.copy()
        input("\nENTER para simular Estándar...")
        resolver_sudoku_simulado(temp)

    if opción in ('2', '3'):
        temp = sud.copy()
        input("\nENTER para simular MRV...")
        resolver_sudoku_mrv_simulado(temp)

    print("\n¡Fin del programa!")


