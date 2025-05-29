import cv2
import numpy as np
import mediapipe as mp
from utils import calculate_angle

def detect(frame, count, stage, pose):
    uyari = False
    dogru = True  # Başlangıçta doğru kabul edelim, hata olursa False yaparız.

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # İskelet çizimi
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

        # Gerekli noktaları al
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        # Açıları hesapla
        left_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
        right_angle = calculate_angle(right_elbow, right_shoulder, right_hip)

        # Açıları yazdır
        cv2.putText(frame, str(int(left_angle)),
                    tuple(np.multiply(left_shoulder, [frame.shape[1], frame.shape[0]]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, str(int(right_angle)),
                    tuple(np.multiply(right_shoulder, [frame.shape[1], frame.shape[0]]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Açı eşikleri
        angle_threshold_up = 160
        angle_threshold_down = 90

        # Başlangıç aşamasını ayarla
        if stage is None:
            stage = "down"

        # Yeni Aşama ve Uyarı Mantığı
        if left_angle > angle_threshold_up and right_angle > angle_threshold_up: # YUKARI Pozisyon
            if stage == 'going_up': # Eğer yukarı çıkıyorduk ve ulaştıysak -> TEKRAR
                count += 1
                dogru = True
            stage = "up"
            uyari = False
        elif left_angle < angle_threshold_down and right_angle < angle_threshold_down: # AŞAĞI Pozisyon
            if stage == 'going_up': # Eğer yukarı çıkıyorduk ama AŞAĞIYA döndüysek -> HATA!
                uyari = True
                dogru = False
            else: # Normal iniş veya zaten aşağıda olma durumu -> HATA YOK
                uyari = False
                dogru = True
            stage = "down"
        else: # ORTA Pozisyon (90-160)
            if stage == 'down':
                stage = 'going_up' # Aşağıdan geliyorsak -> 'going_up'
            elif stage == 'up':
                stage = 'going_down' # Yukarıdan geliyorsak -> 'going_down'
            # Eğer zaten 'going_up' veya 'going_down' isek, aşamayı koru.
            uyari = False # Orta pozisyonda olmak henüz bir hata değil.
            dogru = True

    # 'uyari' True ise, 'dogru' False olmalı.
    if uyari:
        dogru = False

    return frame, count, stage, uyari, dogru