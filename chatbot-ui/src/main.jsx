// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';          // ← make sure this is here
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
