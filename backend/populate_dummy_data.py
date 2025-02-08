# populate_dummy_data.py
import json
import random
from db import get_db_connection, init_db

REALISTIC_COMPLAINTS = [
    "Pests are destroying my wheat crop. Need pesticide recommendations.",
    "Severe drought in my area has reduced my rice yield.",
    "Soil quality has deteriorated; I suspect overuse of chemicals.",
    "Too much rainfall caused waterlogging in my paddy fields.",
    "Fertilizer prices have increased beyond my budget.",
    "Irrigation system is broken, leading to uneven watering.",
    "Electricity cuts affect my water pump, lowering crop yield.",
    "My tomato plants are infected with a virus. Need urgent help.",
    "Low market prices for maize are making farming unsustainable.",
    "Poor seed quality led to low germination this season.",
    "Cattle are damaging my fields due to broken fencing.",
    "There's a fungal infection spreading in my sugarcane crop.",
    "Wild boars are invading my farm and eating young sprouts.",
    "Heavy winds damaged my banana trees just before harvest.",
    "Unexpected frost has severely impacted my mustard field.",
    "Pesticide overuse is harming soil fertility and earthworms.",
    "Subsidy for fertilizers hasn't been released yet.",
    "Mango trees are not flowering; suspect nutrient deficiency.",
    "Excess rainfall has delayed my wheat harvest significantly.",
    "Poor road connectivity is making it hard to transport produce."
]

def populate_dummy_data(num_entries=10):
    """
    Inserts `num_entries` random complaints with:
      - Realistic text
      - Random lat/long (approx India)
      - Random 5D embedding (for demonstration)
    """
    conn = get_db_connection()
    
    for _ in range(num_entries):
        complaint_text = random.choice(REALISTIC_COMPLAINTS)
        lat = round(random.uniform(20.0, 30.0), 4)
        lon = round(random.uniform(70.0, 80.0), 4)

        # Generate a random 5D embedding
        fake_embedding = [round(random.uniform(-1, 1), 3) for _ in range(5)]
        embedding_json = json.dumps(fake_embedding)

        conn.execute("""
            INSERT INTO complaints (text, latitude, longitude, embedding, cluster_id)
            VALUES (?, ?, ?, ?, ?)
        """, (complaint_text, lat, lon, embedding_json, None))
    
    conn.commit()
    conn.close()
    print(f"Inserted {num_entries} dummy complaints.")

if __name__ == "__main__":
    init_db()  # Ensure table exists
    populate_dummy_data(num_entries=20)
