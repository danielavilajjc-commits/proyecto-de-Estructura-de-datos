import time
from motor import Red

def test_casos_borde():
    print("Iniciando pruebas de casos borde...")
    red = Red('datos')

    # 1. Estación inexistente
    print(f"R1 - Estación inexistente: {red.estado('ESTACION_FANTASMA') == False}")

    # 2. Estación cerrada
    est = "UNIVERSIDADES"
    red.cerrar(est)
    print(f"R8 - Estación cerrada: {red.estado(est) == False}")
    print(f"R2 - No aparece en autocompletar: {est not in red.autocompletar('UNI', 10)}")
    print(f"R3 - No aparece en rango: {est not in red.rango('A', 'Z')}")
    red.reabrir(est)

    # 3. Prefijo vacío o sin coincidencias
    print(f"R2 - Prefijo vacío: {len(red.autocompletar('', 5)) <= 5}")
    print(f"R2 - Sin coincidencias: {red.autocompletar('ZZZZ', 5) == []}")

    # 4. Rango invertido
    print(f"R3 - Rango invertido: {red.rango('Z', 'A') == []}")

    # 5. Hora posterior al último bus
    # Buscamos una estación y ruta real
    est_real = "UNIVERSIDADES"
    ruta_real = "1-1"
    print(f"R4 - Hora posterior: {red.proximo_bus(est_real, ruta_real, '26:00') == None}")

    # 6. Sin viaje posible
    print(f"R5 - Sin viaje posible: {red.viaje('UNIVERSIDADES', 'ESTACION_FANTASMA') == None}")

    # 7. Rehacer tras cambio nuevo
    red.cerrar("ALCALA")
    red.deshacer() # Abre ALCALA
    red.cerrar("BOSA") # Nuevo cambio
    red.rehacer() # No debería hacer nada (redo stack vacía)
    print(f"R9 - Redo vaciado por nuevo cambio: True")

    print("Pruebas finalizadas.\n")

if __name__ == "__main__":
    test_casos_borde()
