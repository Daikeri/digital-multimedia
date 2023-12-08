import cv2
import numpy as np

# объект VideoCapture для подключения к IP-камере
url = "http://192.168.43.1:8080/video"

# Открываем поток с камеры
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # преобразование кадра в формат HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # определение диапазона красного цвета в HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    print(mask1)


    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Объединение двух масок
    mask = cv2.bitwise_or(mask1, mask2)

    # применение маски на кадр(побитовая операция И между изображениями)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('Original_video', frame)
    cv2.imshow('HSV_video', hsv)
    cv2.imshow('Result_video', res)

    # нажатие клавиши esc для выхода из цикла
    if cv2.waitKey(1) & 0xFF == 27:
        break

# освобождение ресурсов окна
cap.release()
cv2.destroyAllWindows()
