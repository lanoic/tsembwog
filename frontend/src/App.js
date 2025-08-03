
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get('http://localhost:8000/')
      .then(response => setMessage(response.data.message))
      .catch(error => setMessage("Error connecting to backend"));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Energy Aggregation Platform</h1>
      <p>Status: {message}</p>
    </div>
  );
}

export default App;
