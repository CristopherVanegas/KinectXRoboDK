import cv2
import mediapipe as mp
import numpy as np
from rtde import rtde
import time

# Establecer la conexión con RoboDK
RDK = Robolink()

# Iniciar el paquete RTDE para la comunicación en tiempo real con el robot
rtde_c = rtde.RTDE(RDK)

# Conectar al controlador del robot
rtde_c.connect()

# Obtener el paquete de control
robot = rtde_c.get_controller()

# Inicializar el módulo Mediapipe para el seguimiento de pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Definir la matriz de transformación de la cámara al brazo
camera_to_robot_transform = np.array([[1, 0, 0, 100],   # ajustar los valores para la traslación en x, y, z
                                     [0, 1, 0, 50],
                                     [0, 0, 1, 200],
                                     [0, 0, 0, 1]])

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configurar el modelo de detección de pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No se pudo abrir la cámara.")
            break

        # Convertir la imagen de BGR a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Realizar la detección de la pose
        results = pose.process(image)

        # Dibujar landmarks en la imagen
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Obtener las coordenadas de las articulaciones relevantes
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Convertir las coordenadas de la cámara a coordenadas del brazo robot
            shoulder_cam_coords = np.array([right_shoulder.x, right_shoulder.y, right_shoulder.z, 1])
            elbow_cam_coords = np.array([right_elbow.x, right_elbow.y, right_elbow.z, 1])
            wrist_cam_coords = np.array([right_wrist.x, right_wrist.y, right_wrist.z, 1])

            shoulder_robot_coords = list(np.matmul(camera_to_robot_transform, shoulder_cam_coords)[:3])
            elbow_robot_coords = list(np.matmul(camera_to_robot_transform, elbow_cam_coords)[:3])
            wrist_robot_coords = list(np.matmul(camera_to_robot_transform, wrist_cam_coords)[:3])

            # Mover las articulaciones del brazo del robot en tiempo real
            robot.moveJ(shoulder_robot_coords + [0, 0, 0], 5, 0.5)
            robot.moveJ(elbow_robot_coords + [0, 0, 0], 5, 0.5)
            robot.moveJ(wrist_robot_coords + [0, 0, 0], 5, 0.5)

        # Mostrar la imagen con el seguimiento de la pose
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
