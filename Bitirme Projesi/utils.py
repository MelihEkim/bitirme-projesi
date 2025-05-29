import cv2
import numpy as np
import math

# Üç noktadan açı hesaplar (örneğin: omuz-dirsek-bilek)
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle

# Kalan süreyi çizer
def draw_timer(frame, minutes, seconds):
    timer_text = f"Kalan: {minutes:02}:{seconds:02}"
    cv2.putText(frame, timer_text, (frame.shape[1] - 200, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

# Doğru yapılan harekette ekranda yeşil başarı işareti çizer
def draw_success(frame):
    cv2.circle(frame, (frame.shape[1] - 40, 40), 20, (0, 255, 0), -1)
    cv2.line(frame, (frame.shape[1] - 48, 40), (frame.shape[1] - 42, 46), (255, 255, 255), 2)
    cv2.line(frame, (frame.shape[1] - 42, 46), (frame.shape[1] - 32, 30), (255, 255, 255), 2)

# Hatalı harekette ekranda kırmızı uyarı işareti ve bandı çizer (GÜNCELLENDİ)
def draw_warning(frame, message="Dikkat ediniz!"):
    """
    Kullanıcı hata yaptığında ekrana kırmızı bir uyarı bandı
    ve bir mesaj çizer.
    """
    h, w, _ = frame.shape
    # Kırmızı bir uyarı bandı (ekranın altında)
    cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 255), -1) # Kırmızı renk (BGR)
    # Uyarı metni (beyaz renkte)
    cv2.putText(frame, message, (10, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # Ekrana bir uyarı ikonu (sağ üst köşe - opsiyonel)
    cv2.putText(frame, "!", (w - 50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)