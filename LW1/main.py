import math

import cv2
import numpy as np



def task_2():
    image_path = 'C:\Python_Project\DigitalMultimedia\LW1\picture\DRZlm3lQtMo.jpg'

    window_flags = [cv2.WINDOW_NORMAL, cv2.WINDOW_AUTOSIZE, cv2.WINDOW_FULLSCREEN]

    image_read_flags = [cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE, cv2.IMREAD_UNCHANGED]

    for window_flag in window_flags:
        for read_flag in image_read_flags:

            image = cv2.imread(image_path, read_flag)

            cv2.namedWindow('Image Window', window_flag)

            cv2.imshow('Image Window', image)

            # Ждем, пока пользователь не нажмет клавишу 'q' для завершения
            key = cv2.waitKey(0)
            if key == ord('q'):
                break

    # Закрываем все окна OpenCV
    cv2.destroyAllWindows()

def task_3():
    # Путь к видеофайлу
    video_path = 'C:\Python_Project\DigitalMultimedia\LW1\picture\Top 5 Rat.mp4'

    # Создаем объект VideoCapture
    cap = cv2.VideoCapture(video_path)


    # Проверяем, успешно ли открыто видео
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        cv2.imshow('Video Window', frame)

        key = cv2.waitKey(25)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def task_4():
    input_video_path = 'C:\Python_Project\DigitalMultimedia\LW1\picture\Top 5 Rat.mp4'

    # Создаем объект VideoCapture для чтения видео
    cap = cv2.VideoCapture(input_video_path)

    # Проверяем, успешно ли открыто видео
    if not cap.isOpened():
        print("Error: Could not open input video.")
        exit()

    # Определение размеров видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Параметры для создания объекта VideoWriter
    output_video_path = './output_video.avi'
    fourcc = 'XVID'  # или другой кодек, например, 'MJPG'
    fps = 25.0  # частота кадров в новом видео

    # Создаем объект VideoWriter для записи видео
    out = cv2.VideoWriter(output_video_path, 0, fps, (width, height))

    # Чтение видео кадр за кадром и запись в новый файл
    while True:
        ret, frame = cap.read()

        # Проверяем, успешно ли прочитан кадр
        if not ret:
            break

        # Записываем кадр в новый файл
        out.write(frame)

    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def task_5():
    import cv2

    # Путь к изображению
    image_path = 'C:\Python_Project\DigitalMultimedia\LW1\picture\DRZlm3lQtMo.jpg'

    # Чтение изображения
    img = cv2.imread(image_path)

    # Перевод изображения в формат HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('BGR Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('HSV Image', cv2.WINDOW_NORMAL)


    # Отображение изображения в формате BGR
    cv2.imshow('BGR Image', img)

    # Отображение изображения в формате HSV
    cv2.imshow('HSV Image', img_hsv)

    # Ожидание нажатия клавиши для закрытия окон
    cv2.waitKey(0)

    # Закрытие всех окон
    cv2.destroyAllWindows()

def draw_pentagram_with_circle(image, center, size, color, thickness):
    points = []
    for i in range(5):
        x = int(center[0] + size * math.cos(2 * math.pi * i / 5))
        y = int(center[1] + size * math.sin(2 * math.pi * i / 5))
        points.append((x, y))
    for i in range(5):
        cv2.line(image, points[i], points[(i + 2) % 5], color, thickness)

    # Рисование круга в центре пентаграммы
    cv2.circle(image, center, size // 1, color, thickness)

def task6():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        height, width, _ = frame.shape

        pentagram_image = np.copy(frame)
        center = (width // 2, height // 2)
        size = 100  # Размер пентаграммы
        color = (0, 0, 255)  # Красный цвет
        thickness = 15  # Толщина линий

        draw_pentagram_with_circle(pentagram_image, center, size, color, thickness)

        cv2.imshow('Pentagram with Circle', pentagram_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def task_7():
    # Открываем вебкамеру
    video_capture = cv2.VideoCapture(0)  # 0 - индекс вебкамеры, можно указать другой индекс, если у вас несколько камер

    # Проверяем, успешно ли открыта вебкамера
    if not video_capture.isOpened():
        print("Ошибка при открытии вебкамеры")
        exit()

    # Получаем размеры кадра
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))

    # Определяем кодек и создаем объект VideoWriter для записи видео в файл
    out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                          (frame_width, frame_height))

    # Отображаем видео с вебкамеры и записываем его в файл
    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Не удалось считать кадр с вебкамеры")
            break

        # Отображаем кадр
        cv2.imshow('Webcam', frame)

        # Записываем кадр в файл
        out.write(frame)

        # Проверяем, была ли нажата клавиша 'q', чтобы выйти из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

    # Демонстрируем записанное видео
    recorded_video = cv2.VideoCapture('output_video.avi')

    while True:
        ret, frame = recorded_video.read()

        if not ret:
            print("Не удалось считать кадр из записанного видео")
            break

        # Отображаем записанное видео
        cv2.imshow('Recorded Video', frame)

        # Проверяем, была ли нажата клавиша 'q', чтобы выйти из цикла
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы записанного видео
    recorded_video.release()
    cv2.destroyAllWindows()


def closest_color(b, g, r):
    # Find the closest primary color based on BGR values
    color_distances = {
        'blue': abs(b - 255) + abs(g) + abs(r),
        'green': abs(b) + abs(g - 255) + abs(r),
        'red': abs(b) + abs(g) + abs(r - 255)
    }
    closest = min(color_distances, key=color_distances.get)
    return closest


def determine_pentagram_color(image, center):
    # Check the closest primary color for the central pixel
    b, g, r = image[center[1], center[0]]
    closest_color_name = closest_color(b, g, r)

    # Set the color based on the closest primary color
    if closest_color_name == 'blue':
        return 255, 0, 0  # Blue
    elif closest_color_name == 'green':
        return 0, 255, 0  # Green
    elif closest_color_name == 'red':
        return 0, 0, 255  # Red
    else:
        return 0, 0, 255  # Default to red if no match

def task_8():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        height, width, _ = frame.shape

        pentagram_image = np.copy(frame)
        center = (width // 2, height // 2)
        size = 100  # Pentagram size
        thickness = 15  # Line thickness

        color = determine_pentagram_color(pentagram_image, center)
        draw_pentagram_with_circle(pentagram_image, center, size, color, thickness)

        cv2.imshow('Pentagram with Circle', pentagram_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def task_9():
    import cv2

    # Замените этот URL своим URL-адресом MJPEG-потока
    url = "http://192.168.43.1:8080/video"

    # Открываем поток с камеры
    cap = cv2.VideoCapture(url)

    # Проверяем, успешно ли открыт поток
    if not cap.isOpened():
        print("Не удалось открыть камеру. Убедитесь, что IP-адрес и порт правильные.")
        exit()

    # Отображаем видео
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Не удалось считать кадр с камеры.")
            break

        cv2.imshow('IPWebcam', frame)

        # Если вы хотите закрыть окно, просто нажмите 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()


