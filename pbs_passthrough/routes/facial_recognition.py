from flask import Blueprint, request, jsonify
import os
import base64
from static.helpers import FacialRecognition, convert_image_to_bytea

bp = Blueprint("facial-recognition", __name__)

facial_recognition = FacialRecognition()

@bp.route("/facial-recognition", methods=["POST"])
def perform_facial_regonition():
    if "image" not in request.files:
        return jsonify({"error": "No image file in request"}), 400
    
    image_file = request.files["image"]
    image_path = os.path.join("/tmp", "temp_image.jpg")
    image_file.save(image_path)

    # run facial recognition pipeline
    boxed_image, scores, embeddings = facial_recognition.embedding_pipeline(image_path)

    # create list of embedding strings 
    embedding_strings = []
    for embedding in embeddings:
        embedding_string = ", ".join(map(str, embedding))
        embedding_strings.append(embedding_string)

    # encode image 
    image_bytes = convert_image_to_bytea(boxed_image)
    encoded_boxed_image = base64.b64encode(image_bytes).decode('utf-8')

    results = {
        "boxed_image": encoded_boxed_image,
        "embeddings": embedding_strings
    }

    os.remove(image_path)

    return jsonify(results)