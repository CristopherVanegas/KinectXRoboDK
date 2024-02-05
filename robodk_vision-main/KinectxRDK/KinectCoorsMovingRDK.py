import robolink  # API de RoboDK para Python
import time  # Para añadir pausas si es necesario
import pickle  # Para deserializar datos desde un archivo binario

# Ruta al archivo de coordenadas binarias y a la estación de RoboDK
archivo_coordenadas_bin = r'C:\Users\usuario\Documents\source\repos\KinectXRoboDK\robodk_vision-main\KinectxRDK\coordenadas_kinect.bin'
archivo_estacion = r'C:\Users\usuario\Documents\source\repos\KinectXRoboDK\robodk_vision-main\ESTACION KR10.rdk'

# Iniciar RoboDK
RDK = robolink.Robolink()

# Abrir la estación de RoboDK
RDK.AddFile(archivo_estacion)
RDK.Render(True)  # Actualizar la vista de RoboDK

# Obtener el robot
robot = RDK.Item('', robolink.ITEM_TYPE_ROBOT)

# Leer las coordenadas del archivo binario
with open(archivo_coordenadas_bin, 'rb') as file:
    datos_coordenadas = pickle.load(file)

# Función para mover el robot a una posición
def mover_robot_a(coordenada):
    x, y, z = coordenada['x'], coordenada['y'], coordenada['z']
    
    # Asegúrate de obtener el objeto target correctamente
    target = RDK.Item('Target', robolink.ITEM_TYPE_TARGET)  # Ajusta 'Target' según sea necesario
    
    if not target.Valid():
        print("El target no es válido. Por favor, verifica el nombre y tipo.")
        return
    
    pose = target.Pose()
    pose.setPos([x, y, z, pose[3], pose[4], pose[5]])
    target.setPose(pose)
    robot.MoveJ(target)

# Bucle principal para mover el robot
while True:  # Remover o ajustar este bucle según sea necesario
    for coord in datos_coordenadas:
        mover_robot_a(coord)
        time.sleep(1)  # Ajustar el tiempo de espera según sea necesario

    # Pausa o condición de parada aquí si es un bucle finito
