import numpy as np
import cv2

# изображение
image = cv2.imread('image1.jpg', cv2.IMREAD_COLOR)


def gaussian(x, y, sigma):
    return 1 / (2 * np.pi * sigma ** 2) * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))


def tasks1and2():
    size = 7 # Размерность матрицы (3x3)
    sigma = 2.0  # Среднеквадратичное отклонение

    # Создаем матрицу Гаусса
    gaussian_matrix = np.zeros((size, size))
    center = size // 2  # Центр матрицы

    for x in range(size):
        for y in range(size):
            gaussian_matrix[x, y] = gaussian(x - center, y - center, sigma)

    print("gaussian_matrix\n", gaussian_matrix)

    normalized_matrix = gaussian_matrix / np.sum(gaussian_matrix)
    print("\nnormalized_matrix\n", normalized_matrix)

    return normalized_matrix


def task3():
    # Примените фильтр Гаусса
    blurred_image = cv2.filter2D(image, -1, tasks1and2())

    # Сохраните результат
    cv2.imwrite('blurred_image.jpg', blurred_image)


def task4():
    # Параметры для первой фильтрации
    sigma1 = 0.5
    size1 = 3

    # Создайте матрицу Гаусса и нормализуйте ее
    gaussian_matrix1 = np.zeros((size1, size1))
    center1 = size1 // 2

    for x in range(size1):
        for y in range(size1):
            gaussian_matrix1[x, y] = (1 / (2 * np.pi * sigma1 ** 2)) * np.exp(
                -((x - center1) ** 2 + (y - center1) ** 2) / (2 * sigma1 ** 2))

    normalized_matrix1 = gaussian_matrix1 / np.sum(gaussian_matrix1)

    # Примените фильтр Гаусса с первыми параметрами
    blurred_image1 = cv2.filter2D(image, -1, normalized_matrix1)

    # Параметры для второй фильтрации
    sigma2 = 2.0
    size2 = 7

    # Создайте матрицу Гаусса и нормализуйте ее
    gaussian_matrix2 = np.zeros((size2, size2))
    center2 = size2 // 2

    for x in range(size2):
        for y in range(size2):
            gaussian_matrix2[x, y] = (1 / (2 * np.pi * sigma2 ** 2)) * np.exp(
                -((x - center2) ** 2 + (y - center2) ** 2) / (2 * sigma2 ** 2))

    normalized_matrix2 = gaussian_matrix2 / np.sum(gaussian_matrix2)

    # Примените фильтр Гаусса с вторыми параметрами
    blurred_image2 = cv2.filter2D(image, -1, normalized_matrix2)

    # Сохраните результаты
    cv2.imwrite('blurred_image1.jpg', blurred_image1)
    cv2.imwrite('blurred_image2.jpg', blurred_image2)


def task5():
    # Параметры для первой фильтрации
    sigma1 = 0.5
    size1 = 3

    # Примените встроенную функцию размытия Гаусса
    blurred_image1_opencv = cv2.GaussianBlur(image, (size1, size1), sigma1)

    # Параметры для второй фильтрации
    sigma2 = 2.0
    size2 = 7

    # Примените встроенную функцию размытия Гаусса
    blurred_image2_opencv = cv2.GaussianBlur(image, (size2, size2), sigma2)

    # Сохраните результаты
    cv2.imwrite('blurred_image1_opencv.jpg', blurred_image1_opencv)
    cv2.imwrite('blurred_image2_opencv.jpg', blurred_image2_opencv)

task5()