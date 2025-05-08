import os
import time
import random
import numpy as np
from time import perf_counter

# -------------------------------------------------------------------
# Utilidades de consola y visualización
# -------------------------------------------------------------------

# Limpia la consola según el sistema operativo
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Imprime el tablero en formato legible, con divisiones de bloques 3x3
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

# Limpia consola, muestra mensaje y estado actual del tablero con retardo
def mostrar_estado(tablero, mensaje="", delay=0.03):
    limpiar_consola()
    if mensaje:
        print(mensaje)
    imprimir_tablero(tablero)
    time.sleep(delay)

# -------------------------------------------------------------------
# Creación y validación del tablero Sudoku
# -------------------------------------------------------------------

# Crea un tablero vacío (9x9 lleno de ceros)
def crear_tablero():
    return np.zeros((9, 9), dtype=int)

# Verifica si colocar 'num' en (fila, col) es válido según reglas del Sudoku
def es_valido(tablero, fila, col, num):
    if num in tablero[fila] or num in tablero[:, col]:
        return False
    f0, c0 = (fila // 3) * 3, (col // 3) * 3  
    if num in tablero[f0:f0+3, c0:c0+3]:
        return False
    return True

# Devuelve las coordenadas de todas las celdas vecinas (misma fila, columna, bloque)
def obtener_vecinos(i, j):
    vecinos = set((x, j) for x in range(9) if x != i)
    vecinos.update((i, x) for x in range(9) if x != j)
    f0, c0 = (i // 3) * 3, (j // 3) * 3
    vecinos.update((f0 + x, c0 + y) for x in range(3) for y in range(3) if (f0 + x, c0 + y) != (i, j))
    return vecinos

# -------------------------------------------------------------------
# Generación de Sudoku y solución por backtracking básico
# -------------------------------------------------------------------

# Rellena el tablero de forma aleatoria con una solución válida usando backtracking
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

# Genera un Sudoku con un número determinado de casillas vacías
def generar_sudoku(casillas_vacias):
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
# Algoritmo de backtracking estándar
# -------------------------------------------------------------------

# Resuelve el Sudoku con backtracking simple
def backtracking_estandar(tablero, simular=False, delay=0.03):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if simular:
                            mostrar_estado(tablero, "Simulación Estándar", delay)
                        if backtracking_estandar(tablero, simular, delay):
                            return True
                        tablero[i][j] = 0  
                        if simular:
                            mostrar_estado(tablero, "Retroceso Estándar", delay)
                return False
    return True

# -------------------------------------------------------------------
# Algoritmo de backtracking mejorado con heurísticas (MRV + LCV + Degree)
# -------------------------------------------------------------------

# Inicializa los candidatos posibles (valores válidos por celda vacía)
def inicializar_candidatos(tablero):
    return {
        (i, j): [n for n in range(1, 10) if es_valido(tablero, i, j, n)]
        for i in range(9) for j in range(9) if tablero[i][j] == 0
    }

# Selecciona la celda vacía con menos valores posibles (MRV: Minimum Remaining Values), si hay empate, elige la que tenga más 
#celdas afectadas/vecinos vacíos (Degree Heuristic).
def seleccionar_celda(candidatos):
    min_valores_posibles = min(len(valores) for valores in candidatos.values())  
    celdas_con_menor_dominio = [pos for pos in candidatos if len(candidatos[pos]) == min_valores_posibles]
    return max(celdas_con_menor_dominio,key=lambda pos: sum(1 for vecino in obtener_vecinos(*pos) if vecino in candidatos))


# LCV (Least Constraining Value): ordena primero aquellos valores que aparecen con menor frecuencia en los vecinos, ya que son más 
# probables y menos restrictivos.
def ordenar_por_lcv(celda, candidatos):
    vecinos = obtener_vecinos(*celda)
    valor_impacto = {
        val: sum(1 for v in vecinos if v in candidatos and val in candidatos[v])
        for val in candidatos[celda]
    }
    return sorted(valor_impacto, key=valor_impacto.get)

# Versión optimizada del backtracking con heurísticas (MRV + Degree + LCV)
def backtracking_mejorado(tablero, candidatos=None, simular=False, delay=0.03):
    if candidatos is None:
        candidatos = inicializar_candidatos(tablero)
    if not candidatos:
        return True  

    celda = seleccionar_celda(candidatos)
    i, j = celda

    for valor in ordenar_por_lcv(celda, candidatos):
        tablero[i][j] = valor
        if simular:
            mostrar_estado(tablero, "Simulación Backtracking Mejorado", delay)

        
        nuevos_candidatos = {k: v[:] for k, v in candidatos.items()}
        del nuevos_candidatos[celda]
        for v in obtener_vecinos(i, j):
            if v in nuevos_candidatos and valor in nuevos_candidatos[v]:
                nuevos_candidatos[v].remove(valor)
                if not nuevos_candidatos[v]:
                    break  
        else:
            if backtracking_mejorado(tablero, nuevos_candidatos, simular, delay):
                return True

        tablero[i][j] = 0  
        if simular:
            mostrar_estado(tablero, "Retroceso Backtracking Mejorado", delay)

    return False

# -------------------------------------------------------------------
# Interfaz de usuario y ejecución
# -------------------------------------------------------------------

# Simula la resolución paso a paso mostrando visualmente el progreso
def simular_resolucion(tablero, modo, funcion):
    temp = tablero.copy()
    input(f"\nENTER para simular {modo}...")
    t0 = perf_counter()
    funcion(temp)
    t1 = perf_counter()
    print(f"\nTiempo de visualización {modo}: {t1 - t0:.6f} s")
    input("\nPresiona Enter para regresar al menú.")

# Menú principal del programa
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
        print("3) Simulación  Backtracking Estándar")
        print("4) Simulación Backtracking Mejorado")
        print("5) Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            limpiar_consola()
            imprimir_tablero(sudoku)
            input("\nPresiona Enter para regresar al menú.")
        
        elif opcion == "2":
            limpiar_consola()
            copia1 = sudoku.copy()
            backtracking_estandar(copia1)
            print("\nSolución (Backtracking Estándar):")
            imprimir_tablero(copia1)

            t1 = perf_counter()
            backtracking_estandar(sudoku.copy())
            t1 = perf_counter() - t1

            t2 = perf_counter()
            backtracking_mejorado(sudoku.copy())
            t2 = perf_counter() - t2

            print(f"\nTiempo Backtracking Estándar: {t1:.6f} s")
            print(f"Tiempo Backtracking Mejorado: {t2:.6f} s")
            input("\nPresiona Enter para regresar al menú.")
        
        elif opcion == "3":
            limpiar_consola()
            simular_resolucion(sudoku, "Backtracking Estándar", lambda t: backtracking_estandar(t, simular=True))
        
        elif opcion == "4":
            limpiar_consola()
            simular_resolucion(sudoku, "Backtracking Mejorado", lambda t: backtracking_mejorado(t, simular=True))
        
        elif opcion == "5":
            print("¡Fin del programa!")
            break

if __name__ == "__main__":
    main()
