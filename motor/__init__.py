from .red import Red

def simular_fila(llegadas, frecuencia, capacidad):
    """
    R10: Simulación de fila de abordaje.
    llegadas: lista de (hora, pasajero_id)
    frecuencia: buses por hora
    capacidad: cupo por bus
    """
    # Para manejar cientos de miles de pasajeros, evitamos pop(0)
    pasajeros_esperando = llegadas # Asumimos que ya vienen ordenados por hora
    idx_cola = 0
    total_abordados = 0

    # Calculamos el intervalo entre buses en minutos
    intervalo_bus = 60 / frecuencia if frecuencia > 0 else float('inf')

    # Tiempo actual en minutos desde el inicio (00:00)
    tiempo_actual = 0
    bus_actual_tiempo = 0

    while idx_cola < len(pasajeros_esperando):
        # Mientras el tiempo avanza hasta el próximo bus
        while bus_actual_tiempo < tiempo_actual:
            bus_actual_tiempo += intervalo_bus

        # Llegar al tiempo del primer pasajero en cola
        hora_llegada_str = pasajeros_esperando[idx_cola][0]
        h, m = map(int, hora_llegada_str.split(':'))
        tiempo_llegada = h * 60 + m

        # Avanzar el tiempo a la llegada del pasajero o al próximo bus
        tiempo_actual = tiempo_llegada

        # El bus llega en bus_actual_tiempo
        # Todos los que llegaron antes o en el tiempo del bus pueden subir
        while idx_cola < len(pasajeros_esperando):
            h_l, m_l = map(int, pasajeros_esperando[idx_cola][0].split(':'))
            t_l = h_l * 60 + m_l

            if t_l <= bus_actual_tiempo:
                # Este pasajero puede subir al bus actual si hay cupo
                # Pero necesitamos saber cuántos subieron YA en este bus
                break
            else:
                # El pasajero llega después del bus actual
                break

        # Lógica de abordaje del bus actual
        cupo_restante = capacidad
        while idx_cola < len(pasajeros_esperando):
            h_l, m_l = map(int, pasajeros_esperando[idx_cola][0].split(':'))
            t_l = h_l * 60 + m_l

            if t_l <= bus_actual_tiempo and cupo_restante > 0:
                total_abordados += 1
                cupo_restante -= 1
                idx_cola += 1
            else:
                break

        # Pasar al siguiente bus
        bus_actual_tiempo += intervalo_bus

    return total_abordados
