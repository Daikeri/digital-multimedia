import cv2
import numpy as np


# Task 1
def read_and_preprocess_image(file_path):
    # Read the image
    image = cv2.imread(file_path)

    # Convert to black and white
    bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the original and preprocessed images
    # cv2.imshow("Original Image", image)
    cv2.imshow("Preprocessed Image", bw_image)

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(bw_image, (5, 5), 0.5)

    # Display the blurred image
    cv2.imshow("Blurred Image", blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blurred_image


# Task 2
def calculate_gradients(image):
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    gradient_angle = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

    print(gradient_magnitude)
    print()
    print(gradient_angle)
    return gradient_magnitude, gradient_angle
# Task 3
def non_maximum_suppression(magnitude, angle):
    # Suppress non-maximums
    rows, cols = magnitude.shape
    result_image = np.zeros_like(magnitude)
    print(angle)

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
    cv2.imshow("Non-Maximum Suppression", result_image)
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
def perform_experiment(file_path):
    gradient_thresholds = (30, 60)

    # Task 1
    blurred_image = read_and_preprocess_image(file_path)

    # Task 2
    gradient_magnitude, gradient_angle = calculate_gradients(blurred_image)

    # Task 3
    suppressed_image = non_maximum_suppression(gradient_magnitude, gradient_angle)

    # Task 4
    result_image = double_thresholding(suppressed_image, *gradient_thresholds)


# Example usage:
image_file_path = "C:\Python_Project\DigitalMultimedia\LW4\img.png"
perform_experiment(image_file_path)
