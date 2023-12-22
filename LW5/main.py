import cv2

# Функция для обработки кадра
def process_frame(old_frame, new_frame):
    # Перевести в чернобелый цвет
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    # Применить размытие Гаусса
    old_blur = cv2.GaussianBlur(old_gray, (15, 15), 0)
    new_blur = cv2.GaussianBlur(new_gray, (15, 15), 0)

    # Найти разницу между двумя кадрами
    frame_diff = cv2.absdiff(old_blur, new_blur)

    # Провести операцию двоичного разделения
    _, threshold = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Найти контуры объектов
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)

    # Проверить контуры и записать кадр, если есть движение
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Порог площади контура для определения движения
            return True  # Есть движение

    return False  # Нет движения

# Открыть видеофайл для чтения
video_capture = cv2.VideoCapture('C:\Python_Project\DigitalMultimedia\LW5\ЛР4_main_video.mov')

# Прочитать первый кадр
ret, old_frame = video_capture.read()

# Проверить успешность чтения первого кадра
if not ret:
    print("Не удалось прочитать первый кадр. Проверьте видеофайл.")
    exit()

# Подготовить файл для записи
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (old_frame.shape[1], old_frame.shape[0]))

# Начать цикл обработки видео
while True:
    # Скопировать старый кадр
    old_frame_copy = old_frame.copy()

    # Прочитать новый кадр
    ret, new_frame = video_capture.read()

    # Проверить успешность чтения нового кадра
    if not ret:
        print("Достигнут конец видеофайла.")
        break

    # Проверить наличие движения
    if process_frame(old_frame, new_frame):
        # Если есть движение, записать кадр в файл
        output_video.write(new_frame)

    # Отобразить видео
    #cv2.imshow('Video', new_frame)

    # Обновить старый кадр
    old_frame = new_frame

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освободить ресурсы
video_capture.release()
output_video.release()
cv2.destroyAllWindows()
