import tensorflow as tf

def download_data():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()
    return (train_images, train_labels), (test_images, test_labels)

if __name__ == "__main__":
    download_data()