from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def generar_numero_aleatorio():
    return np.random.randint(1, 11)

if rank == 0:
    numero_secreto = np.random.randint(1, 11)
    print(f"Número secreto generado por el manager: {numero_secreto}")

    intentos = 0
    adivino_alguien = False

    while not adivino_alguien:
        for i in [1, 2]:
            intento_worker = comm.recv(source=i)
            intentos += 1
            if intento_worker == numero_secreto:
                adivino_alguien = True
                print(f"Worker {i} adivina: {intento_worker}")
                # Enviar señal de parada a ambos workers utilizando -1
                for j in [1, 2]:
                    comm.send(-1, dest=j)
                break
            else:
                # Enviar el número secreto de vuelta si no es correcto
                comm.send(numero_secreto, dest=i)

    print(f"Número de intentos hasta adivinar: {intentos}")

else:
    # Bucle hasta que alguien adivine el número
    while True:
        intento = generar_numero_aleatorio()
        comm.send(intento, dest=0)
        respuesta = comm.recv(source=0)
        if respuesta == -1:
            break
