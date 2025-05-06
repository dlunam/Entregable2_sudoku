import os
import time
import random
import numpy as np
from time import perf_counter

# -------------------------------------------------------------------
# Utilidades
# -------------------------------------------------------------------

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tablero(tablero):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            val = tablero[i][j]
            print(val if val != 0 else ".", end=" ")
        print()

def mostrar_estado(tablero, mensaje="", delay=0.03):
    limpiar_consola()
    if mensaje:
        print(mensaje)
    imprimir_tablero(tablero)
    time.sleep(delay)

# -------------------------------------------------------------------
# Tablero y validación
# -------------------------------------------------------------------

def crear_tablero():
    return np.zeros((9, 9), dtype=int)

def es_valido(tablero, fila, col, num):
    if num in tablero[fila] or num in tablero[:, col]:
        return False
    f0, c0 = (fila // 3) * 3, (col // 3) * 3
    if num in tablero[f0:f0+3, c0:c0+3]:
        return False
    return True

def obtener_vecinos(i, j):
    vecinos = set((x, j) for x in range(9) if x != i)
    vecinos.update((i, x) for x in range(9) if x != j)
    f0, c0 = (i // 3) * 3, (j // 3) * 3
    vecinos.update((f0 + x, c0 + y) for x in range(3) for y in range(3) if (f0 + x, c0 + y) != (i, j))
    return vecinos

# -------------------------------------------------------------------
# Generación y resolución
# -------------------------------------------------------------------

def rellenar_sudoku(tablero):
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

def resolver_sudoku(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[i][j] = 0
                return False
    return True

# -------------------------------------------------------------------
# MRV + LCV + Degree
# -------------------------------------------------------------------

def inicializar_dominios(tablero):
    return {
        (i, j): [n for n in range(1, 10) if es_valido(tablero, i, j, n)]
        for i in range(9) for j in range(9) if tablero[i][j] == 0
    }

def seleccionar_celda(dominios):
    min_dom = min(len(v) for v in dominios.values())
    candidatas = [pos for pos in dominios if len(dominios[pos]) == min_dom]
    return max(candidatas, key=lambda pos: sum(1 for v in obtener_vecinos(*pos) if v in dominios))

def ordenar_por_lcv(celda, dominios):
    vecinos = obtener_vecinos(*celda)
    valor_impacto = {
        val: sum(1 for v in vecinos if v in dominios and val in dominios[v])
        for val in dominios[celda]
    }
    return sorted(valor_impacto, key=valor_impacto.get)

def resolver_mrv(tablero, dominios=None, simular=False, delay=0.03):
    if dominios is None:
        dominios = inicializar_dominios(tablero)
    if not dominios:
        return True
    celda = seleccionar_celda(dominios)
    i, j = celda
    for valor in ordenar_por_lcv(celda, dominios):
        tablero[i][j] = valor
        if simular:
            mostrar_estado(tablero, "Simulación MRV", delay)

        nuevos_dominios = {k: v[:] for k, v in dominios.items()}
        del nuevos_dominios[celda]
        for v in obtener_vecinos(i, j):
            if v in nuevos_dominios and valor in nuevos_dominios[v]:
                nuevos_dominios[v].remove(valor)
                if not nuevos_dominios[v]:
                    break
        else:
            if resolver_mrv(tablero, nuevos_dominios, simular, delay):
                return True
        tablero[i][j] = 0
        if simular:
            mostrar_estado(tablero, "Retroceso MRV", delay)
    return False

# -------------------------------------------------------------------
# Simulación visual estándar
# -------------------------------------------------------------------

def resolver_sudoku_simulado(tablero, delay=0.03):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        mostrar_estado(tablero, "Simulación Estándar", delay)
                        if resolver_sudoku_simulado(tablero, delay):
                            return True
                        tablero[i][j] = 0
                        mostrar_estado(tablero, "Retroceso Estándar", delay)
                return False
    return True

# -------------------------------------------------------------------
# Ejecución principal con interfaz
# -------------------------------------------------------------------

def simular_resolucion(tablero, modo, funcion):
    temp = tablero.copy()
    input(f"\nENTER para simular {modo}...")
    funcion(temp)

def main():
    while True:
        limpiar_consola()
        try:
            n = int(input("¿Cuántas casillas vacías quieres en el Sudoku (0–81)?: "))
            if 0 <= n <= 81:
                break
            print("Debe estar entre 0 y 81.")
        except ValueError:
            print("Introduce un número válido.")

    sudoku, solucion = generar_sudoku(n)

    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1) Mostrar Sudoku")
        print("2) Resolver Sudoku (mostrar solución y tiempos)")
        print("3) Simulación Estándar")
        print("4) Simulación MRV Mejorado")
        print("5) Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            limpiar_consola()
            imprimir_tablero(sudoku)
            input("\nPresiona Enter para regresar al menú.")
        
        elif opcion == "2":
            limpiar_consola()
            copia1 = sudoku.copy()
            resolver_sudoku(copia1)
            print("\nSolución (Backtracking Estándar):")
            imprimir_tablero(copia1)

            t1 = perf_counter()
            resolver_sudoku(sudoku.copy())
            t1 = perf_counter() - t1

            t2 = perf_counter()
            resolver_mrv(sudoku.copy())
            t2 = perf_counter() - t2

            print(f"\nTiempo Estándar: {t1:.6f} s")
            print(f"Tiempo MRV Mejorado: {t2:.6f} s")
            input("\nPresiona Enter para regresar al menú.")
        
        elif opcion == "3":
            limpiar_consola()
            simular_resolucion(sudoku, "Estándar", resolver_sudoku_simulado)
        
        elif opcion == "4":
            limpiar_consola()
            simular_resolucion(sudoku, "MRV", lambda t: resolver_mrv(t, simular=True))
        
        elif opcion == "5":
            print("¡Fin del programa!")
            break

if __name__ == "__main__":
    main()
