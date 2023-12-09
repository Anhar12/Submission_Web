import os
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from PIL import Image
import tempfile

app = Flask(__name__)

# Declare Model and Class
class_labels = ['Broccoli','KembangKol','Kentang','Kubis','Labu','Lobak','Paprika','Pare','Telur','Terung','Timun','Tomato','Wortel','Ayam','Sapi']
model = load_model("yourModel")

# Cors Handling if using web
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# backend Code for Prediction using image processing
@app.route("/predict", methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name) # save
        
        # Open and Resize image
        images = Image.open(temp_file.name)
        images = images.resize((150, 150)) # bisa disesuaikan dengan format model

        # Preprocess the image
        images = image.img_to_array(images)
        images = tf.keras.applications.mobilenet_v2.preprocess_input(images)
        images = tf.expand_dims(images, axis=0)
        
        # Predict image
        predictions = model.predict(images)
        predicted_class = tf.argmax(predictions, axis=1)[0].numpy()

        # Delete temp file
        temp_file.close()

        response = {   
            "message": "success",
            "result": class_labels[predicted_class],
            "id": predicted_class.tolist(),
            "score" : predictions[0][predicted_class].tolist()
        }
        
        if predictions[0][predicted_class] > 0.9 and predictions[0][predicted_class]  <= 1.0:
            return jsonify(response), 201
        else:
            return jsonify({"error": f"Prediksi gagal, gambar tidak terdeteksi"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


if __name__ =='__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 3000)))