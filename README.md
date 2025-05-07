# Sudoku Solver & Visualizer

## Descripción

Este proyecto en Python genera tableros de Sudoku aleatorios y los resuelve utilizando dos enfoques de **backtracking**: uno estándar y otro mejorado con heurísticas (MRV, Degree y LCV). Además, incluye una simulación visual paso a paso para observar cómo se resuelve el tablero.

---

# Estructura del código
## 1. Utilidades de Consola y Visualización

* `limpiar_consola`: Limpia la consola según el sistema operativo.
* `imprimir_tablero`: Imprime el tablero con separaciones visuales por bloques 3x3.
* `mostrar_estado`: Muestra el estado actual del tablero con un mensaje y un pequeño retardo para las simulaciones.


## 2. Creación y Validación del Tablero

* `crear_tablero`: Devuelve una matriz 9x9 con ceros.
* `es_valido`: Verifica si un número puede colocarse en una celda sin violar las reglas del Sudoku (filas, columnas, subcuadros).
* `obtener_vecinos`: Calcula las celdas vecinas a una dada (en la misma fila, columna o subcuadro 3x3).


## 3. Generación y Solución de Tableros

* `rellenar_sudoku`: Rellena el tablero completamente utilizando backtracking para asegurar que tiene solución.
* `generar_sudoku`: Crea un tablero parcialmente vacío a partir de una solución completa, garantizando un número dado de casillas vacías.


## 4. Algoritmos de Solución

### 4.1 Backtracking Estándar

* `backtracking_estandar`: Implementación clásica sin optimizaciones, explora todas las combinaciones posibles de forma recursiva.

### 4.2 Backtracking Mejorado (con heurísticas)

* `backtracking_mejorado`: Algoritmo optimizado que utiliza:

  * MRV (Minimum Remaining Values)
  * Degree Heuristic (celdas con más vecinos vacíos)
  * LCV (Least Constraining Value)

Funciones auxiliares:

* `inicializar_candidatos`: Mapea cada celda vacía con sus valores posibles.
* `seleccionar_celda`: Escoge la celda más restringida según MRV y Degree.
* `ordenar_por_lcv`: Ordena los valores de una celda de forma que se minimice la restricción sobre otras.


## 5. Simulación Visual Paso a Paso

* `simular_resolucion`: Ejecuta una simulación visual del algoritmo seleccionado mostrando los cambios paso a paso.


## 6. Interfaz de Usuario (CLI)

* `main`: Función principal que proporciona un menú de opciones en consola para:
  - Generar un nuevo tablero con casillas vacías definidas por el usuario.
  - Resolver el Sudoku usando ambos algoritmos y comparar tiempos.
  - Ejecutar visualizaciones paso a paso.


---

## Requisitos

* Python 3.7 o superior
* Bibliotecas:

  * `numpy`



## Cómo usarlo

1. **Ejecutar el script:**

```bash
python sudoku_solver.py
```

2. **Interacción a través del menú:**

   * Mostrar el tablero generado
   * Resolver el Sudoku con ambos métodos y comparar los tiempos de ejecución
   * Visualizar paso a paso la resolución con ambos métodos

---

## Ejemplo de uso

```text
¿Cuántas casillas vacías quieres en el Sudoku (0–81)?: 30

=== MENÚ DE OPCIONES ===
1) Mostrar Sudoku
2) Resolver Sudoku (mostrar solución y tiempos)
3) Simulación Backtracking Estándar
4) Simulación Backtracking Mejorado
5) Salir
```

---

## Algoritmos utilizados

### Backtracking Estándar

El algoritmo básico de **backtracking** recursivo prueba diferentes valores en las celdas vacías y retrocede cuando no encuentra una solución válida, probando con valores diferentes.

### Backtracking Mejorado

Este algoritmo optimiza el proceso utilizando las siguientes heurísticas:

---

* **MRV (Minimum Remaining Values)**: Prioriza la celda con menos valores posibles para reducir el espacio de búsqueda.
* **Degree Heuristic**: En caso de empate en MRV, selecciona la celda con mayor número de celdas vecinas afectadas.
* **LCV (Least Constraining Value)**: Selecciona, entre todos los candidatos (valores posibles para una casilla), aquel que menos restricciones impone a las celdas vecinas. Es decir, se elige el valor que, al asignarse, elimina la menor cantidad de opciones en los candidatos de las demás casillas afectadas (misma fila, columna o región en un Sudoku).

  En términos de frecuencia: si un candidato aparece en pocas celdas posibles (tiene menor frecuencia entre los valores válidos de la casilla actual y sus vecinas), es más probable que ese valor deba ir en esta casilla, ya que está más limitado en dónde puede colocarse.
  
  **Ejemplo (Sudoku)**:  
  Supón que una casilla tiene como candidatos los valores {4, 7, 9}, y estos valores también aparecen en las celdas vecinas de esta forma:
  - El 4 aparece en 6 casillas vecinas.
  - El 7 en 3 casillas vecinas.
  - El 9 en 8 casillas vecinas.
  
  En este caso, el 7 sería el mejor candidato según LCV, ya que eliminaría menos opciones de los vecinos y, por lo tanto, impone menos restricciones. Además, como el 7 aparece en menos lugares posibles, es más probable que deba colocarse aquí, ya que tiene menos alternativas disponibles en el resto del tablero.

---

# Comparación entre Fuerza Bruta y Backtracking
La fuerza bruta intenta explorar las 9⁸¹ combinaciones posibles, lo cual sería extremadamente costoso en tiempo y recursos. En cambio, el backtracking avanza casilla por casilla, retrocede cuando se incumplen las reglas del Sudoku y permite aplicar técnicas heurísticas. Por eso, es una solución mucho más eficiente y efectiva. 

---

# Aplicaciones del Backtracking

Algunas aplicaciones del algoritmo de backtracking incluyen:

**Logística**: Se usa para identificar las rutas más eficientes en la distribución de productos. El algoritmo prueba distintas combinaciones de rutas y descarta aquellas que no cumplen con los requisitos como el tiempo o el coste.

**Ciberseguridad**: En la detección de vulnerabilidades o en el proceso de descifrado de códigos, el backtracking es útil para probar todas las combinaciones posibles de claves o configuraciones.
