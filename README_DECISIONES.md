# README de Decisiones - Planeador de Viajes TransMilenio

## Análisis de Complejidad y Estructuras (R12)

| Requisito | Operación | Complejidad | $n$ | Decisión Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `estado` | $O(1)$ | Estaciones | Diccionario (Hash Table) para acceso instantáneo. |
| **R2** | `autocompletar` | $O(\log n + k)$ | Estaciones | Árbol AVL para mantener orden alfabético y búsqueda rápida de prefijos. |
| **R3** | `rango` | $O(\log n + m)$ | Estaciones | Recorrido In-Order del AVL entre dos límites. |
| **R4** | `proximo_bus` | $O(\log h)$ | Horas | Merge Sort inicial + Búsqueda Binaria propia sobre la lista de horas. |
| **R5** | `viaje` | $O(V+E)$ | Red | BFS simple buscando rutas directas o con un solo transbordo. |
| **R6** | `ranking` | $O(1)$ / $O(E)$ | Estaciones | Caché de resultados. Se recalcula solo si la red cambia (cerrar/abrir/editar). |
| **R7** | `ediciones` | $O(1)$ / $O(n)$ | Paradas | Lista Doblemente Enlazada para inserción/borrado eficiente tras ubicación. |
| **R8** | `cerrar/reabrir` | $O(\log n)$ | Estaciones | Marcador booleano en el nodo del AVL y en el diccionario. |
| **R9** | `undo/redo` | $O(1)$ | Cambios | Dos Pilas independientes para gestionar la historia de operaciones. |
| **R10**| `simular_fila` | $O(P)$ | Pasajeros | Procesamiento lineal de llegadas con punteros para evitar desplazar la lista. |

## Decisiones sobre Datos

### Manejo de Horas (> 24:00)
En el estándar GTFS, las horas como `25:10` representan la 1:10 AM del día siguiente. Se ha decidido manejar las horas como **strings** en formato `HH:MM`. 
**Justificación:** Dado que el formato es fijo (dos dígitos para hora y minuto), la comparación léxica de strings (`"25:10" > "23:50"`) es idéntica a la comparación numérica, lo que permite usar Merge Sort y Búsqueda Binaria sin conversiones costosas.

## Restricciones de Implementación
Se ha evitado estrictamente el uso de `sorted()`, `.sort()`, `min()`, `max()` sobre colecciones, `bisect`, `heapq` y cualquier librería externa, implementando cada algoritmo y estructura desde cero.
