import cv2
import mediapipe as mp
import pygame
import threading
import os

# === CONFIGURACIÓN DE RUTAS ===
base_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(base_path)

fa = os.path.join(parent_path, "sources/fa.wav")
la = os.path.join(parent_path, "sources/la.wav")
la_sos = os.path.join(parent_path, "sources/la_sostenido.wav")
re_sos = os.path.join(parent_path, "sources/re_sostenido.wav")

sonidos = [fa, la, la_sos, re_sos]

# === FUNCIONES AUXILIARES ===
def is_finger_down(landmarks, finger_tip, finger_mcp):
    """Devuelve True si el dedo está bajado (tip más abajo que la base)."""
    return landmarks[finger_tip].y > landmarks[finger_mcp].y

def play_sonido(indice):
    """Reproduce un sonido en un hilo independiente."""
    pygame.mixer.Sound(sonidos[indice]).play()

# === CONFIGURACIÓN DE MEDIAPIPE Y PYGAME ===
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pygame.mixer.init()

# === INICIO DE CAPTURA DE CÁMARA ===
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2  # Máximo 2 manos
) as hands:
    
    # Estado de cada dedo: 4 dedos por mano * 2 manos = 8 posibles dedos
    finger_state = [False] * (2 * 4)
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignorando frame vacío de la cámara.")
            continue

        # Procesamiento de la imagen
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Dibujo de manos y detección de dedos
        if results.multi_hand_landmarks:
            for h, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                finger_tips = [4, 8, 12, 16]   # Pulgar, índice, medio, anular
                finger_mcp = [1, 5, 9, 13]

                for i in range(4):  # 4 dedos
                    finger_index = i + h * 4  # índice global del dedo
                    if is_finger_down(hand_landmarks.landmark, finger_tips[i], finger_mcp[i]):
                        if not finger_state[finger_index]:
                            # Reproducir el sonido solo una vez cuando baja
                            threading.Thread(target=play_sonido, args=(i,), daemon=True).start()
                            finger_state[finger_index] = True
                    else:
                        finger_state[finger_index] = False

        # Mostrar imagen con efecto espejo
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
        # Salir con tecla ESC
        if cv2.waitKey(5) & 0xFF == 27:
            break

# === LIMPIEZA ===
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
