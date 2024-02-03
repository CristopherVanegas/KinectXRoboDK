import cv2
import mediapipe as mp
import numpy as np
import time

# Inicializar MediaPipe Hands y Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Función para guardar las coordenadas en un archivo de texto
def guardar_coordenadas(coordenadas):
    with open("coordenadas.txt", "w") as file:
        file.write("\n".join(coordenadas))

coordenadas = []

# Tiempo de inicio
inicio_tiempo = time.time()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convertir el color de BGR a RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Procesar la imagen para detectar pose
    pose_results = pose.process(image)

    # Convertir el color de vuelta a BGR para mostrarlo
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Dibujar la pose
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = pose_results.pose_landmarks.landmark
        
        # Identificar los puntos de interés (codo y muñeca)
        codo = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        muneca = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        if codo and muneca:
            # Obtener las coordenadas del codo y la muñeca
            x_codo, y_codo, _ = int(codo.x * image.shape[1]), int(codo.y * image.shape[0]), codo.z
            x_muneca, y_muneca, _ = int(muneca.x * image.shape[1]), int(muneca.y * image.shape[0]), muneca.z

            # Calcular los movimientos del codo y la muñeca
            movimiento_x = x_muneca - x_codo
            movimiento_y = y_muneca - y_codo

            coordenadas = [f"Codo: x={x_codo}, y={y_codo}, Muñeca: x={x_muneca}, y={y_muneca}",
                           f"Movimiento: x={movimiento_x}, y={movimiento_y}"]

            # Guardar las coordenadas en el archivo de texto
            guardar_coordenadas(coordenadas)

            # Imprimir las coordenadas cada 2 segundos
            tiempo_actual = time.time()
            if tiempo_actual - inicio_tiempo >= 2.0:
                inicio_tiempo = tiempo_actual
                for coord in coordenadas:
                    print(coord)

    cv2.imshow('Detector de codo y muñeca', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
