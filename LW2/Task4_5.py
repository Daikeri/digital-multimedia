import cv2
import numpy as np

# объект VideoCapture для подключения к IP-камере
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

    # вычисление момента на основе маски
    moments = cv2.moments(mask)

    # поиск момента первого порядка
    area = moments['m00']

    if area > 0:
        # ширина и высота прямоугольника равны квадратному корню из площади объекта
        width = height = int(np.sqrt(area))
        # вычисление координат центра объекта на изображении с использованием момент первого порядка
        c_x = int(moments["m10"] / moments["m00"])
        c_y = int(moments["m01"] / moments["m00"])
        # отрисовка прямоугольника
        color = (0, 0, 0) # черный цвет
        thickness = 2 # толщина

        cv2.line(
            frame,
            (c_x - (width // 16), c_y),
            (c_x + (width // 16), c_y),
            (0, 0, 0),
            2
        )
        cv2.line(
            frame,
            (c_x, c_y - (height // 16)),
            (c_x, c_y + (height // 16)),
            (0, 0, 0),
            2
        )

    cv2.imshow('HSV_frame', hsv)
    cv2.imshow('Result_frame', frame)

    # нажатие клавиши esc для выхода из цикла
    if cv2.waitKey(1) & 0xFF == 27:
        break

print("Площадь объекта:", area)

# освобождение ресурсов окна
cap.release()
cv2.destroyAllWindows()

