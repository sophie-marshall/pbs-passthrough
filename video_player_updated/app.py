from flask import Flask, render_template, send_file, jsonify, request
from dotenv import load_dotenv
import os 
import boto3
import psycopg2
import json 
import base64
from utils.facial_recognition import FacialRecognition
from utils.helpers import convert_image_to_bytea


# load env files
load_dotenv()

# define an app 
app = Flask(__name__)

# instantiate class 
facial_regonition = FacialRecognition()

# create s3 client 
s3 = boto3.client("s3", 
                  region_name="us-east-1", 
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

S3_BUCKET = "pbs-passthrough"

# create a base route 
@app.route("/")
def index():
    # get a list of videos available 
    response = s3.list_objects_v2(Bucket=S3_BUCKET)
    video_files = [obj['Key'].split('/')[-1] for obj in response.get('Contents', [])]

    # render the appropriate html template 
    return render_template("home.html", video_files=video_files)

# create a route that will play a selected video 
@app.route("/passthrough/<filename>")
def passthrough(filename):
    # renter video player 
    return render_template("passthrough.html", filename=filename)

# create a route for serving videos 
@app.route("/videos/<filename>")
def serve_video(filename):
    response = s3.get_object(Bucket=S3_BUCKET, Key=filename)
    return send_file(response["Body"], mimetype="video/mp4")

# create a facial recognition route 
@app.route("/facial-recognition", methods=["POST"])
def perform_facial_regonition():
    if "image" not in request.files:
        return jsonify({"error": "No image file in request"}), 400
    
    image_file = request.files["image"]
    image_path = os.path.join("/tmp", "temp_image.jpg")
    image_file.save(image_path)

    # run facial recognition pipeline
    boxed_image, scores, embeddings = facial_regonition.embedding_pipeline(image_path)

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

# create a route to query the db 
@app.route("/query", methods=["POST"])
def query_database():

    # get embeddings from the request
    embeddings = request.json.get("embeddings", [])

    # instantaite a dictionary to hold our results
    all_results = {}

    # iterate over available facial embeddings
    for idx, embedding in enumerate(embeddings):
        
        # connect to db and create cursor
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            database=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            port="5432"
        )
        cur = conn.cursor()

        # define and execute query
        similarity_query = f"SELECT id, actor_actress, about, 1-(facial_embedding <=>'[{embedding}]') AS score FROM masterpiece_grantchester ORDER BY facial_embedding <=> '[{embedding}]' LIMIT 3;"
        cur.execute(similarity_query)

        # get results
        rows = cur.fetchall()

        # format results
        results = [{"id": row[0], "actor_actress": row[1], "about": row[2], "similarity_score": row[3]} for row in rows]

        # close connection
        cur.close()
        conn.close()

        # append to dictionary, keeping track of face number
        all_results[f"face_{idx}"] = results

    return jsonify(all_results)

# start application
if __name__ == "__main__":
    app.run(debug=True)

