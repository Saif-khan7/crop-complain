import json
import numpy as np
from sklearn.cluster import KMeans
from db import get_db_connection

def run_clustering():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, embedding, latitude, longitude FROM complaints").fetchall()
    
    vectors = []
    ids = []

    for row in rows:
        if row["embedding"] is None:
            continue
        try:
            emb = json.loads(row["embedding"])  # parse JSON list
        except:
            continue
        
        # Optionally combine lat/long
        lat = float(row["latitude"] or 0.0)
        lon = float(row["longitude"] or 0.0)

        # If you want lat/long to matter, do something like:
        # combined_vector = emb + [lat/5.0, lon/5.0]
        # The /5.0 is a rough normalization—tweak as needed
        combined_vector = emb

        vectors.append(combined_vector)
        ids.append(row["id"])

    if not vectors:
        conn.close()
        return 0

    X = np.array(vectors)

    # Suppose we want exactly 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(X)

    # Update DB
    for i, label in enumerate(labels):
        cid = int(label)
        complaint_id = ids[i]
        conn.execute("UPDATE complaints SET cluster_id=? WHERE id=?", (cid, complaint_id))

    conn.commit()
    conn.close()
    return 3  # We forced 3 clusters
