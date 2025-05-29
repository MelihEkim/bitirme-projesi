from gtts import gTTS
import os
import playsound
import threading
import time
import uuid # Benzersiz dosya adı için

audio_lock = threading.Lock()

# Güncellenmiş Egzersiz Açıklamaları
ACIKLAMALAR = {
    "squat": "Squat için: Ayaklar omuz genişliğinde açık, sırt düz, kalçayı geriye itin.",
    "pushup": "Şınav için: Vücut düz, dirsekler 90 dereceye inip kalkmalı.",
    "plank": "Plank için: Vücut düz bir çizgi halinde, kalça düşmemeli.",
    "lunge": "Lunge için: Öndeki diz 90 derece olmalı, arka diz yere yaklaşmalı.",
    "jumping_jack": "Jumping Jack için: Kollar yukarı, ayaklar yana zıplayarak açılır ve kapanır.",
    "situp": "Sit-up için: Sırt yere yatık, eller başta, gövdeyi yukarı kaldır.",
    "mountain_climber": "Mountain Climber için: Plank pozisyonunda dizleri sırayla göğse çek.",
    "side_plank": "Side Plank için: Vücut yana dönük düz bir çizgide olmalı.",
    "shoulder_press": "Şoldır pres için: Ağırlıkları omuz hizasından başlayarak, kontrollü şekilde yukarı itin ve yavaşça başlangıç pozisyonuna indirin.",
    "high_knees": "High Knees için: Dizleri sırayla göğse doğru hızlıca kaldır.",
    "dumbbell_curl": "Dambıl körl için: Avuç içleri yukarı bakarken, dirsekleri sabit tutarak ağırlıkları omuzlara bükün, yavaşça indirin.",
    "lateral_raise": "Lateral Raise için: Kollarınızı hafifçe bükerek, ağırlıkları kontrollü bir şekilde omuz seviyesine kadar yanlara doğru kaldırın ve yavaşça indirin.",
    "biceps_hammer_curl": "Hamır körl için: Avuç içleri birbirine bakacak şekilde, dirsekleri vücuda yakın tutarak ağırlıkları omuzlarınıza doğru kaldırın ve yavaşça indirin."
}

def speak(text):
    """ gTTS kullanarak metni seslendirir. """
    with audio_lock:
        filename = f"temp_audio_{uuid.uuid4().hex}.mp3"
        try:
            print(f"gTTS ile seslendiriliyor: {text}")
            tts = gTTS(text=text, lang='tr', slow=False)
            tts.save(filename)
            playsound.playsound(filename)

        except playsound.PlaysoundException as pse:
            print(f"Playsound hatası: {pse}")
        except Exception as e:
            print(f"gTTS veya playsound hatası: {e}")
        finally:
            # Ne olursa olsun dosyayı silmeye çalış
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception as e_rem:
                    print(f"Geçici dosya silinirken hata: {e_rem}")


def stop_audio():
    pass

def speak_exercise_explanation(movement):
    """ Egzersiz açıklamasını seslendirir. """
    tarif_detay = ACIKLAMALAR.get(movement, "Bu hareketin açıklaması bulunamadı.")
    def thread_function():
        time.sleep(0.2)
        speak(tarif_detay)
    threading.Thread(target=thread_function, daemon=True).start()

def speak_congratulations():
    """ Tebrik mesajını seslendirir. """
    message = "Tebrikler, doğru yaptınız!"
    def thread_function():
        time.sleep(0.2)
        speak(message)
    threading.Thread(target=thread_function, daemon=True).start()

def create_audio_feedback(text):
    """ Genel (veya uyarı) geri bildirimlerini seslendirir. """
    def thread_function():
        time.sleep(0.2)
        speak(text)
    threading.Thread(target=thread_function, daemon=True).start()