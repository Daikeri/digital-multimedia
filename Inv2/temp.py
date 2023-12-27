import cv2
import numpy as np
import os

# Task 1
def read_and_preprocess_image(file_path, k_size):
    # Read the image
    image = cv2.imread(file_path)

    # Convert to black and white
    bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the original and preprocessed images
    # cv2.imshow("Original Image", image)
    #cv2.imshow("Preprocessed Image", bw_image)

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(bw_image, (k_size, k_size), 0.)

    # Display the blurred image
    #cv2.imshow("Blurred Image", blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blurred_image


# Task 2
def calculate_gradients(image, operator):
    gradient_x = None
    gradient_y = None
    if operator == 'sobel':
        gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    elif operator == 'prewitt':
        gradient_x = cv2.Scharr(image, cv2.CV_64F, 1, 0)
        gradient_y = cv2.Scharr(image, cv2.CV_64F, 0, 1)
    elif operator == 'roberts':
        gradient_x = cv2.filter2D(image, cv2.CV_64F, np.array([[1, 0], [0, -1]]))
        gradient_y = cv2.filter2D(image, cv2.CV_64F, np.array([[0, 1], [-1, 0]]))


    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    gradient_magnitude_uint8 = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    gradient_angle = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

    return gradient_magnitude_uint8, gradient_angle
# Task 3
def non_maximum_suppression(magnitude, angle):
    # Suppress non-maximums
    rows, cols = magnitude.shape
    result_image = np.zeros_like(magnitude)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            angle_val = angle[i, j]

            # Declare neighbors before if-else statements
            neighbors = []

            if (0 <= angle_val < 22.5) or (337.5 <= angle_val <= 360):  # четко правый
                neighbors = [magnitude[i, j - 1], magnitude[i, j + 1]]
            elif 22.5 <= angle_val < 67.5:  # правый верхний диагональный
                neighbors = [magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]]
            elif 67.5 <= angle_val < 112.5:  # четко вверх
                neighbors = [magnitude[i - 1, j], magnitude[i + 1, j]]
            elif 112.5 <= angle_val < 157.5:  # левый верхний диагональный
                neighbors = [magnitude[i - 1, j + 1], magnitude[i + 1, j - 1]]
            elif 157.5 <= angle_val < 202.5:  # четко влево
                neighbors = [magnitude[i, j - 1], magnitude[i, j + 1]]
            elif 202.5 <= angle_val < 247.5:  # левый нижний диагональный
                neighbors = [magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]]
            elif 247.5 <= angle_val < 292.5:  # четко вниз
                neighbors = [magnitude[i - 1, j], magnitude[i + 1, j]]
            elif 292.5 <= angle_val < 337.5:  # правый нижний диагональный
                neighbors = [magnitude[i - 1, j + 1], magnitude[i + 1, j - 1]]

            if len(neighbors) != 0:
                max_neighbor = max(neighbors)

                if magnitude[i, j] >= max_neighbor:
                    result_image[i, j] = magnitude[i, j]

    # Display the resulting image
    #cv2.imshow("Non-Maximum Suppression", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result_image


# Task 4
def double_thresholding(image, low_threshold, high_threshold):
    # Apply double thresholding
    edges = np.zeros_like(image)
    strong_edges = (image > high_threshold)
    weak_edges = (image >= low_threshold) & (image <= high_threshold)

    edges[strong_edges] = 255
    edges[weak_edges] = 0  # You can adjust this value as needed

    # Display the resulting image after double thresholding
    cv2.imshow("Double Thresholding", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return edges


# Task 5
def perform_experiment(file_path, gauss_ker_size, gradient_thresholds, operator):

    # Task 1
    blurred_image = read_and_preprocess_image(file_path, gauss_ker_size)

    # Task 2
    gradient_magnitude, gradient_angle = calculate_gradients(blurred_image, operator)

    # Task 3
    suppressed_image = non_maximum_suppression(gradient_magnitude, gradient_angle)

    # Task 4
    result_image = double_thresholding(suppressed_image, *gradient_thresholds)


def process_images_in_directory(directory_path):
    # Получаем список всех файлов в указанной директории
    image_files = [f for f in os.listdir(directory_path) if f.endswith('.png') or f.endswith('.jpg')]

    # Проходим по каждому файлу
    for image_file in image_files:
        image_file_path = os.path.join(directory_path, image_file)

        # Проходим по всем возможным значениям параметров
        for k_size in [3, 5, 7]:  # Размер ядра Гауссова размытия
            for thresholds in [(10, 20), (20, 40), (30, 60)]:  # Пороги для двойного порогового преобразования
                for operator in ['sobel']:  # Операторы вычисления градиента 'prewitt', 'roberts'
                    # Выполняем эксперимент с текущими параметрами
                    print(
                        f"Processing {image_file} with parameters: k_size={k_size}, thresholds={thresholds}, operator={operator}")
                    perform_experiment(image_file_path, k_size, thresholds, operator)



image_directory_path = "C:\Python_Project\DigitalMultimedia\Inv2\source"
process_images_in_directory(image_directory_path)

