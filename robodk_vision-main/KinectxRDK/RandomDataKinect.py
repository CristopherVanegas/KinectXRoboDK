import random
import pickle

# Función para generar una coordenada aleatoria en el rango especificado
def generar_coordenada():
    return round(random.uniform(-1.0, 1.0), 6)

# Nombres de las posiciones del robot
nombres_posiciones = ["Hombro derecho", "Codo derecho", "Muñeca derecha", "Mano derecha"]

# Preparar los datos para guardar
datos_para_guardar = []

for nombre in nombres_posiciones:
    x = generar_coordenada()
    y = generar_coordenada()
    z = generar_coordenada()

    coordenadas = {"nombre": nombre, "x": x, "y": y, "z": z}
    datos_para_guardar.append(coordenadas)

# Abre el archivo para escritura binaria en la ruta especificada
ruta_archivo_binario = r'C:\Users\usuario\Documents\source\repos\KinectXRoboDK\robodk_vision-main\KinectxRDK\coordenadas_kinect.bin'
with open(ruta_archivo_binario, 'wb') as archivo_bin:
    # Guarda los datos en formato binario
    pickle.dump(datos_para_guardar, archivo_bin)

print("Coordenadas generadas y guardadas en 'coordenadas_kinect.bin'")
