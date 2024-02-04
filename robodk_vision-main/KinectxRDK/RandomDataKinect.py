import random

# Función para generar una coordenada aleatoria en el rango especificado
def generar_coordenada():
    return round(random.uniform(-1.0, 1.0), 6)

# Nombres de las posiciones del robot
nombres_posiciones = ["Hombro derecho", "Codo derecho", "Muñeca derecha", "Mano derecha"]

# Abre el archivo para escritura en la ruta especificada
with open(r'C:\Users\usuario\Documents\source\repos\KinectXRoboDK\robodk_vision-main\KinectxRDK\coordenadas_kinect.txt', 'w') as archivo:

    # Genera y guarda las coordenadas para cada posición del robot
    for nombre in nombres_posiciones:
        x = generar_coordenada()
        y = generar_coordenada()
        z = generar_coordenada()

        coordenadas = f"{nombre} (X, Y, Z): ({x}, {y}, {z})"
        archivo.write(coordenadas + '\n')

print("Coordenadas generadas y guardadas en 'coordenadas_kinect.txt'")
