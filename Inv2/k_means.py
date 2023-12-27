import os
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from skimage import io


def image_segmentation(image, n_clusters=2):
    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pixels)
    labels = kmeans.labels_
    segmented_image = labels.reshape(image.shape[:2])
    return segmented_image


def plot_images(original, segmented, title1='Original Image', title2='Segmented Image'):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title(title1)

    plt.subplot(1, 2, 2)
    plt.imshow(segmented, cmap='viridis')
    plt.title(title2)

    plt.show()


def process_images_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            original_image = io.imread(image_path)
            segmented_image = image_segmentation(original_image)
            plot_images(original_image, segmented_image, title1=f'Original Image - {filename}',
                        title2=f'Segmented Image - {filename}')


# Пример использования
initial_directory = "C:\Python_Project\DigitalMultimedia\Inv2\source"
process_images_in_directory(initial_directory)
