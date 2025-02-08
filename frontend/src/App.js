import React from 'react';
import ComplaintForm from './components/ComplaintForm';
import MapView from './components/MapView';

function App() {
  return (
    <div style={{ margin: '1rem' }}>
      <h1>Complaint Clustering</h1>
      <ComplaintForm />
      <hr />
      <MapView />
    </div>
  );
}

export default App;
