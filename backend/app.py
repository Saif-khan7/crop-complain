# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json

from db import init_db, get_db_connection
from cluster import run_clustering

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

init_db()  # Make sure 'complaints' table exists

@app.route('/')
def home():
    return "Complaint Clustering API is running."

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    """
    Expects JSON:
    {
      "text": "My crops are failing...",
      "latitude": 30.1234,
      "longitude": 76.2345
    }
    1. Generates a random embedding (for demonstration).
    2. Stores complaint in DB with cluster_id=None (initially).
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    complaint_text = data.get("text", "")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not complaint_text or lat is None or lon is None:
        return jsonify({"error": "Please provide text, latitude, and longitude"}), 400

    # Generate a random 5D embedding as a placeholder
    random_embedding = [round(random.uniform(-1, 1), 3) for _ in range(5)]
    embedding_json = json.dumps(random_embedding)

    # Insert into DB
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO complaints (text, latitude, longitude, embedding)
        VALUES (?, ?, ?, ?)
    """, (complaint_text, lat, lon, embedding_json))
    conn.commit()
    conn.close()

    return jsonify({"message": "Complaint submitted successfully"}), 200

@app.route('/run-clustering', methods=['POST'])
def do_clustering():
    """
    Runs DBSCAN (in cluster.py) on existing complaints.
    Embedding + lat/long => cluster_id
    """
    num_clusters = run_clustering()
    return jsonify({"message": f"Clustering complete. #clusters={num_clusters}"}), 200

@app.route('/complaints', methods=['GET'])
def get_complaints():
    """
    Returns all complaint rows:
      [
        {
          "id": ...,
          "text": ...,
          "latitude": ...,
          "longitude": ...,
          "embedding": ...,
          "cluster_id": ...
          "created_at": ...
        },
        ...
      ]
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM complaints").fetchall()
    conn.close()

    complaints = []
    for row in rows:
        complaints.append({
            "id": row["id"],
            "text": row["text"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "embedding": row["embedding"],
            "cluster_id": row["cluster_id"],
            "created_at": row["created_at"]
        })
    return jsonify(complaints)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
