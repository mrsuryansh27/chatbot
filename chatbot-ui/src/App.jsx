// src/App.jsx
import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';

export default function App() {
  // Read URL params
  const params = new URLSearchParams(window.location.search);
  const isEmbed = params.get('embed') === '1';
  const clientId = params.get('client_id') || import.meta.env.VITE_SITE_ID;

  // Local state
  const [open, setOpen] = useState(isEmbed);
  const [mode, setMode] = useState('chat');
  const [branding, setBranding] = useState(null);

  // Fetch branding config in embed mode
  useEffect(() => {
    if (!isEmbed) return;
    fetch(`${import.meta.env.VITE_API_URL}/api/clients/${clientId}`)
      .then(res => res.json())
      .then(data => {
        if (data.branding) setBranding(data.branding);
      })
      .catch(err => console.error('Error fetching client config:', err));
  }, [clientId, isEmbed]);

  // Handle close (only in non-embed)
  const handleClose = () => {
    if (!isEmbed) setOpen(false);
  };

  // --- Demo mode ---
  if (!isEmbed) {
    return (
      <>
        <div className="fixed bottom-6 right-6 flex space-x-2 z-50">
          <button
            className={`bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-full shadow-lg focus:ring-2 ${
              mode === 'chat' ? 'ring-indigo-300' : 'ring-transparent'
            }`}
            onClick={() => { setMode('chat'); setOpen(true); }}
            aria-label="Open Chat"
          >
            💬
          </button>
          <button
            className={`bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-full shadow-lg focus:ring-2 ${
              mode === 'flight' ? 'ring-indigo-300' : 'ring-transparent'
            }`}
            onClick={() => { setMode('flight'); setOpen(true); }}
            aria-label="Open Flight"
          >
            ✈️
          </button>
        </div>

        {open && (
          <div className="fixed bottom-20 right-6 w-80 h-[500px] bg-white dark:bg-gray-800 rounded-xl shadow-2xl flex flex-col overflow-hidden z-50">
            <ChatInterface
              siteId={clientId}
              mode={mode}
              branding={branding}
              onModeChange={setMode}
              onClose={handleClose}
            />
          </div>
        )}
      </>
    );
  }

  // --- Embed mode ---
  return (
    <div className="fixed inset-0 z-50 flex justify-center items-end pointer-events-none">
      <div className="w-full max-w-sm h-[600px] pointer-events-auto">
        <ChatInterface
          siteId={clientId}
          mode={mode}
          branding={branding}
          onModeChange={setMode}
          onClose={() => { /* Parent script toggles iframe */ }}
        />
      </div>
    </div>
  );
}

