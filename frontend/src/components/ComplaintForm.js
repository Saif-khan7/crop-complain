// ComplaintForm.js
import React, { useState, useEffect } from 'react';

const ComplaintForm = () => {
  const [text, setText] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    // Attempt to fetch user’s current location if possible
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLatitude(pos.coords.latitude.toFixed(4));
          setLongitude(pos.coords.longitude.toFixed(4));
        },
        (err) => {
          console.log("Could not get location:", err);
        }
      );
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (!text || !latitude || !longitude) {
      setError("Please fill in complaint text and location");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/submit-complaint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude)
        })
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        setText("");
      } else {
        setError(data.error || "Error submitting complaint");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  const handleClustering = async () => {
    setMessage("");
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:5000/run-clustering", {
        method: "POST"
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
      } else {
        setError(data.error || "Error running clustering");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  return (
    <div style={{ marginBottom: '1rem' }}>
      <h2>Submit a Complaint</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Complaint Text:</label><br />
          <textarea
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ width: "100%" }}
          />
        </div>
        <div>
          <label>Latitude:</label><br />
          <input
            type="number"
            step="0.0001"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
          />
        </div>
        <div>
          <label>Longitude:</label><br />
          <input
            type="number"
            step="0.0001"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
          />
        </div>
        <button type="submit" style={{ marginTop: '8px' }}>
          Submit Complaint
        </button>
      </form>
      <button onClick={handleClustering} style={{ marginTop: '8px' }}>
        Run Clustering
      </button>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default ComplaintForm;
