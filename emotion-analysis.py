import cv2
import numpy as np
from deepface import DeepFace
from tkinter import Tk, Label
from PIL import Image, ImageTk
import threading

POSITIVE_EMOTIONS = {"happy", "surprise"}

def analyze_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        return emotion
    except Exception as e:
        print("Ошибка анализа эмоции:", e)
        return None

def capture_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    return None

def analyze_emotions_average(num_frames=5):
    emotions = []
    for _ in range(num_frames):
        frame = capture_frame()
        if frame is not None:
            emotion = analyze_emotion(frame)
            if emotion:
                emotions.append(emotion)

    if emotions:
        most_common_emotion = max(set(emotions), key=emotions.count)
        print(f"Финальная эмоция: {most_common_emotion}")

def analyze_emotion_on_command():
    while True:
        command = input("Хотите посмотреть товар?")
        if command.lower() == 'Нет':
            break
        analyze_emotions_average(5)

# Настройка основного окна
root = Tk()
root.title("Эмоции")

image_label = Label(root)
image_label.pack()

cap = cv2.VideoCapture(0)

# Запускаем поток для анализа эмоций
command_thread = threading.Thread(target=analyze_emotion_on_command, daemon=True)
command_thread.start()

# Запускаем окно
root.mainloop()

cap.release()
cv2.destroyAllWindows()
