import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands y Pose
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convertir el color de BGR a RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Procesar la imagen para detectar manos y pose
    hand_results = hands.process(image)
    pose_results = pose.process(image)

    # Convertir el color de vuelta a BGR para mostrarlo
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Dibujar la pose (opcionalmente, para ver puntos del brazo)
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Dibujar la mano derecha
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Detector de mano y brazo derecho', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
