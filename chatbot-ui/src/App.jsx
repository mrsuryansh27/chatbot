import React, { useState, useRef, useEffect } from 'react';
import ChatInterface from './ChatInterface';

export default function App() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Toggle Button */}
      <button
        className="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 z-50"
        onClick={() => setOpen(o => !o)}
        aria-label={open ? 'Close chat' : 'Open chat'}
      >
        💬
      </button>

      {/* Chat Widget */}
      {open && (
        <div className="fixed bottom-20 right-6 w-80 h-[500px] bg-white dark:bg-gray-800 rounded-xl shadow-2xl flex flex-col overflow-hidden z-50">
          <ChatInterface
             siteId={import.meta.env.VITE_SITE_ID}
            //  onClose={() => setOpen(false)}
           />
        </div>
      )}
    </>
  );
}
