from flask import Blueprint, request, jsonify
import psycopg2
import os 
from dotenv import load_dotenv

bp = Blueprint("query", __name__)

load_dotenv()

@bp.route("/query", methods=["POST"])
def query_db():

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