import time
import os
from motor import Red

def medir_rendimiento():
    print("Midiendo rendimiento (R11)...")
    red = Red('datos')

    # Medir R1 (Estado)
    start = time.time()
    for _ in range(10000):
        red.estado("UNIVERSIDADES")
    print(f"R1 - Estado (10k consultas): {time.time() - start:.4f}s")

    # Medir R2 (Autocompletar)
    start = time.time()
    for _ in range(1000):
        red.autocompletar("AV", 5)
    print(f"R2 - Autocompletar (1k consultas): {time.time() - start:.4f}s")

    # Medir R4 (Próximo Bus)
    start = time.time()
    for _ in range(1000):
        red.proximo_bus("UNIVERSIDADES", "1-1", "10:00")
    print(f"R4 - Próximo Bus (1k consultas): {time.time() - start:.4f}s")

    # Medir R6 (Ranking)
    start = time.time()
    red.ranking(10) # Primera vez (calcula)
    print(f"R6 - Ranking (1ra vez): {time.time() - start:.4f}s")

    start = time.time()
    red.ranking(10) # Segunda vez (caché)
    print(f"R6 - Ranking (caché): {time.time() - start:.4f}s")

if __name__ == "__main__":
    medir_rendimiento()
