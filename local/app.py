from flask import Flask, jsonify, request
# import tensorflow as tf
from tensorflow import keras
import numpy as np
import time

# Create a Flask app
app = Flask(__name__)

model = None
model_last_loaded = None
model_file_path = "/data/processed/model.h5"
model_reload_interval = 120  # 2 minutes


def load_model():
    global model, model_last_loaded
    model = keras.models.load_model(model_file_path)
    model_last_loaded = time.time()
    print(f"Model loaded from {model_file_path} at {time.ctime(model_last_loaded)}")


load_model()


# Define a predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    global model, model_last_loaded

    # Reload the model if the interval has passed
    if time.time() - model_last_loaded > model_reload_interval:
        print(f"Reloading model at {time.ctime(time.time())}")
        load_model()

    # Parse the input data
    data = request.json
    input_data = np.array(data['input_data'])

    # Make a prediction
    prediction = model.predict(input_data)
    predicted_class = int(np.argmax(prediction))

    # convert int64 to standard integer
    predicted_class = int(predicted_class)

    # Return the predicted class
    return jsonify({'predicted_class': predicted_class})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7007)
