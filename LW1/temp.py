import cv2
import numpy as np

# Функция для размытия изображения внутри прямоугольника
def blur_inside_rectangle(image, rect_start_point, rect_end_point):
    # Копируем изображение, чтобы не изменять оригинал
    blurred_image = image.copy()

    # Определяем координаты прямоугольника
    x1, y1 = rect_start_point
    x2, y2 = rect_end_point

    # Вырезаем область изображения внутри прямоугольника
    roi = blurred_image[y1:y2, x1:x2]

    # Размываем вырезанную область
    blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)

    # Вставляем размытую область обратно в изображение
    blurred_image[y1:y2, x1:x2] = blurred_roi

    return blurred_image

# Функция для отображения контуров прямоугольника
def draw_rectangle_contours(image, rect_start_point, rect_end_point, color):
    # Копируем изображение, чтобы не изменять оригинал
    image_with_contours = image.copy()

    # Определяем координаты прямоугольника
    x1, y1 = rect_start_point
    x2, y2 = rect_end_point

    # Рисуем контуры прямоугольника
    cv2.rectangle(image_with_contours, (x1, y1), (x2, y2), color, 2)

    return image_with_contours

# Захватываем видеопоток с камеры
cap = cv2.VideoCapture(0)

while True:
    # Считываем кадр с камеры
    ret, frame = cap.read()

    # Определяем размеры изображения
    height, width, _ = frame.shape

    # Определяем размеры горизонтального прямоугольника (увеличили длину)
    rect_width_horizontal = 300
    rect_height_horizontal = 50

    # Вычисляем координаты горизонтального прямоугольника для центрирования
    rect_start_x_horizontal = int((width - rect_width_horizontal) / 2)
    rect_start_y_horizontal = int((height - rect_height_horizontal) / 2)
    rect_end_x_horizontal = rect_start_x_horizontal + rect_width_horizontal
    rect_end_y_horizontal = rect_start_y_horizontal + rect_height_horizontal

    # Определяем размеры вертикального прямоугольника
    rect_width_vertical = 50
    rect_height_vertical = 200

    # Вычисляем координаты вертикального прямоугольника для центрирования
    rect_start_x_vertical = int((width - rect_width_vertical) / 2)
    rect_start_y_vertical = int((height - rect_height_vertical) / 2)
    rect_end_x_vertical = rect_start_x_vertical + rect_width_vertical
    rect_end_y_vertical = rect_start_y_vertical + rect_height_vertical

    # Размываем изображение внутри горизонтального прямоугольника
    blurred_frame_horizontal = blur_inside_rectangle(frame, (rect_start_x_horizontal, rect_start_y_horizontal),
                                                     (rect_end_x_horizontal, rect_end_y_horizontal))

    # Рисуем контуры горизонтального прямоугольника
    frame_with_contours_horizontal = draw_rectangle_contours(blurred_frame_horizontal,
                                                             (rect_start_x_horizontal, rect_start_y_horizontal),
                                                             (rect_end_x_horizontal, rect_end_y_horizontal), (0, 0, 255))

    # Размываем изображение внутри вертикального прямоугольника без изменений
    blurred_frame_vertical = frame.copy()

    # Рисуем контуры вертикального прямоугольника
    frame_with_contours_vertical = draw_rectangle_contours(blurred_frame_vertical,
                                                           (rect_start_x_vertical, rect_start_y_vertical),
                                                           (rect_end_x_vertical, rect_end_y_vertical), (0, 0, 255))

    # Объединяем результаты
    result_frame = frame.copy()
    result_frame[rect_start_y_horizontal:rect_end_y_horizontal, rect_start_x_horizontal:rect_end_x_horizontal] = \
        frame_with_contours_horizontal[
            rect_start_y_horizontal:rect_end_y_horizontal, rect_start_x_horizontal:rect_end_x_horizontal]
    result_frame[rect_start_y_vertical:rect_end_y_vertical, rect_start_x_vertical:rect_end_x_vertical] = \
        frame_with_contours_vertical[
            rect_start_y_vertical:rect_end_y_vertical, rect_start_x_vertical:rect_end_x_vertical]

    # Отображаем результат
    cv2.imshow('Frame with Blurred Rectangles', result_frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
