import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css";

// A small array of colored marker URLs from a Google source
// (You can replace with your own images or a local set of icons.)
const clusterIconUrls = [
  "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/orange-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/purple-dot.png"
];

// Return a Leaflet icon for a given cluster_id
function getClusterIcon(clusterId) {
  // If clusterId is missing or negative (like DBSCAN noise), use a gray icon:
  if (clusterId === null || clusterId === undefined || clusterId < 0) {
    return L.icon({
      iconUrl: "http://maps.google.com/mapfiles/ms/icons/ltblue-dot.png",
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    });
  }

  // Otherwise, pick from the array using modulo
  const url = clusterIconUrls[clusterId % clusterIconUrls.length];
  return L.icon({
    iconUrl: url,
    iconSize: [32, 32],
    iconAnchor: [16, 32]
  });
}

const MapView = () => {
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/complaints")
      .then((res) => res.json())
      .then((data) => {
        setComplaints(data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ marginTop: '1rem' }}>
      <h2>Map View (Cluster Colored)</h2>
      <MapContainer
        center={[22.5, 78.5]} // Approximate center of India
        zoom={5}
        style={{ height: "500px", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {complaints.map((c) => {
          if (c.latitude == null || c.longitude == null) return null;

          const lat = parseFloat(c.latitude);
          const lng = parseFloat(c.longitude);

          return (
            <Marker
              key={c.id}
              position={[lat, lng]}
              icon={getClusterIcon(c.cluster_id)}
            >
              <Popup>
                <strong>ID:</strong> {c.id}<br />
                <strong>Text:</strong> {c.text}<br />
                <strong>Cluster:</strong> {c.cluster_id ?? "None"}
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MapView;
