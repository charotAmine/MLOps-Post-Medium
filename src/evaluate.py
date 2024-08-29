import tensorflow as tf
from download_data import download_data
from preprocess_data import preprocess_data

_, (test_images, test_labels) = download_data()
_, test_images = preprocess_data(test_images, test_images)

model = tf.keras.models.load_model("outputs/model")
loss, accuracy = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {accuracy}")
