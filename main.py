import cv2
import mediapipe as mp
import pygame
import threading
import time

do = "recursos/do.wav"
do_sos = "recursos/do_sostenido.wav"
re = "recursos/re.wav"
re_sos = "recursos/re_sostenido.wav"
mi = "recursos/mi.wav"
fa = "recursos/fa.wav"
fa_sos = "recursos/fa_sostenido.wav"
sol = "recursos/sol.wav"
sol_so = "recursos/sol_sostenido.wav"
la = "recursos/la.wav"
la_sos = "recursos/la_sostenido.wav"
si = "recursos/si.wav"

sounds = [do, re , mi, fa ,sol, la, si, do]
sounds_sos = [do_sos, re_sos, mi, fa_sos, sol_so, la_sos, si, do_sos]

def is_finger_down(landmarks, finger_tip, finger_base):
    return landmarks[finger_tip].y > landmarks[finger_base].y

def is_sos(landmarks, nodo_pulgar, referencia_pulgar, hand_label):
    thumb_x = landmarks[nodo_pulgar].x
    ref_x = landmarks[referencia_pulgar].x
    if hand_label == "Right":
        return thumb_x > ref_x
    else:
        return thumb_x < ref_x

def play_sonido(index, sos):
    if sos:
        pygame.mixer.Sound(sounds_sos[index]).play()
        time.sleep(1)
    else:
        pygame.mixer.Sound(sounds[index]).play()
        time.sleep(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pygame.mixer.init()

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=2
) as hands:
    
    finger_state = [False] * 8
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks and results.multi_handedness:
            for h, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[h].classification[0].label
                
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                NODO_PULGAR = 4
                REFERENCIA_PULGAR = 5
                
                fingers_map = []
                
                if hand_label == "Left":
                    fingers_map = [
                        (20, 0),
                        (16, 1),
                        (12, 2),
                        (8, 3)
                    ]
                else:
                    fingers_map = [
                        (8, 4),
                        (12, 5),
                        (16, 6),
                        (20, 7)
                    ]

                sos_active = is_sos(hand_landmarks.landmark, NODO_PULGAR, REFERENCIA_PULGAR, hand_label)

                for tip_id, sound_index in fingers_map:
                    if is_finger_down(hand_landmarks.landmark, tip_id, tip_id - 1):
                        
                        if not finger_state[sound_index]:
                            threading.Thread(target=play_sonido, args=(sound_index, sos_active), daemon=True).start()
                            finger_state[sound_index] = True
                    else:
                        finger_state[sound_index] = False

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()