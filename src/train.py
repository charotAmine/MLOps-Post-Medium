import tensorflow as tf
from model import create_model
from download_data import download_data
from preprocess_data import preprocess_data
import mlflow
import mlflow.tensorflow

class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        mlflow.log_metrics({
           "loss": logs["loss"],
           "accuracy":
               logs["accuracy"]
    })
        
# Start Logging
mlflow.start_run()

# enable autologging
mlflow.tensorflow.autolog()

(train_images, train_labels), (test_images, test_labels) = download_data()
train_images, test_images = preprocess_data(train_images, test_images)

model = create_model()
history = model.fit(train_images, train_labels, epochs=1, validation_data=(test_images, test_labels),callbacks=[CustomCallback()])

model.save("outputs/model")