# Importa la librería de RoboDK para Python
from robolink import *
from robodk import *

# Conecta con el API de RoboDK
RDK = Robolink()

# Carga la estación RoboDK desde la ubicación del archivo
estacion_rdk_path = "C:/Users/usuario/Documents/source/repos/KinectXRoboDK/robodk_vision-main/ESTACION KR10.rdk"
RDK.AddFile(estacion_rdk_path)

# Obtén el robot de la estación actual (asegúrate de que el robot esté cargado en la estación)
robot = RDK.ItemUserPick("Selecciona un robot", ITEM_TYPE_ROBOT)

if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido")

# Crea un programa para el robot
program = RDK.AddProgram("Movimiento en Diferentes Direcciones")

# Definir la cantidad de movimientos y la distancia de cada movimiento
num_movimientos = 5
distancia = 50  # mm

# Bucle para mover el robot en diferentes direcciones
for i in range(num_movimientos):
    # Obtén la posición actual del robot
    current_pose = robot.Pose()
    
    # Calcula una nueva posición desplazándola en la dirección Z
    new_pose = transl(0, 0, distancia * (i + 1)) * current_pose
    
    # Agrega una instrucción de movimiento lineal al programa
    program.MoveL(new_pose)

# Ejecuta la simulación
program.RunProgram()
