import cv2
import numpy as np

# Задание 1: Чтение изображения с камеры и конвертация в формат HSV
cap = cv2.VideoCapture(0)
while not cap.isOpened():
    pass

ret, frame = cap.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Задание 2: Фильтрация изображения и вывод результата
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

lower_red = np.array([160, 100, 100])
upper_red = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv, lower_red, upper_red)

# Объединение двух масок
final_mask = cv2.bitwise_or(mask1, mask2)
filtered_image = cv2.bitwise_and(frame, frame, mask=final_mask)

# Вывод фильтрованного изображения
cv2.imshow("Filtered Image", filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Задание 3: Морфологические преобразования
kernel = np.ones((5, 5), np.uint8)
opened_image = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
closed_image = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)

# Вывод результатов морфологических преобразований
cv2.imshow("Opened Image", opened_image)
cv2.imshow("Closed Image", closed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Задание 4: Нахождение моментов и площади объекта
contours, _ = cv2.findContours(closed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    max_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(max_contour)
    area = moments['m00']
    print(f"Площадь объекта: {area}")

    # Задание 5: Нахождение центра и построение прямоугольника
    if area > 0:
        cx = int(moments['m10'] / area)
        cy = int(moments['m01'] / area)

        # Построение черного прямоугольника вокруг объекта
        black_rect = np.zeros_like(frame)
        cv2.rectangle(black_rect, (cx - 50, cy - 50), (cx + 50, cy + 50), (0, 0, 0), 2)

        # Вывод видео с черным прямоугольником
        while True:
            ret, frame = cap.read()
            cv2.imshow("Black Rectangle Tracking", frame + black_rect)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
else:
    print("Объект не найден.")
