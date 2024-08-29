import json
import os
import tensorflow as tf

def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR", default=""),
                              "model")

    model = tf.keras.models.load_model(model_path)


def run(raw_data):
    data = json.loads(raw_data)
    predictions = model.predict(data['data'])
    return json.dumps(predictions.tolist())