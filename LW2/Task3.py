import cv2
import numpy as np

# объект VideoCapture для подключения к IP-камере
url = "http://192.168.43.1:8080/video"

# Открываем поток с камеры
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # определение диапазона красного цвета в HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Объединение двух масок
    mask = cv2.bitwise_or(mask1, mask2)

    # применение маски на изображение
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # структурирующий элемент(определяет размер и форму области)
    kernel = np.ones((5, 5), np.uint8)

    # применение операции открытия - позволяет удалить шумы и мелкие объекты на изображении(удаление нежелательных пикселей или деталей)
    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)

    # применение операции закрытия - позволяет заполнить маленькие пробелы и разрывы в объектах на изображении
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Opening', opening)
    cv2.imshow('Closing', closing)

    # нажатие клавиши esc для выхода из цикла
    if cv2.waitKey(1) & 0xFF == 27:
        break

# освобождение ресурсов окна
cap.release()
cv2.destroyAllWindows()
