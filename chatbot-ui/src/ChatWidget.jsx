import React, { useState, useEffect, useRef } from 'react';

export default function ChatWidget({ onClose }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi there! What’s your name?' }
  ]);
  const [input, setInput] = useState('');
  const [step, setStep] = useState(1);
  const [userInfo, setUserInfo] = useState({});
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef();

  // auto-scroll on new message
  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [messages]);

  const postMessage = async (userText) => {
    setMessages(m => [...m, { sender: 'user', text: userText }]);
    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      setMessages(m => [
        ...m,
        { sender: 'bot', text: `You said: "${userText}"` }
      ]);
      setLoading(false);
    }, 800);
  };

  const handleSend = () => {
    const text = input.trim();
    if (!text) return;
    setInput('');

    // Simple onboarding flow
    if (step <= 3) {
      const prompts = [
        'Thanks! What’s your phone number?',
        'Great, and your email?',
        'Done! How can I help you today?'
      ];
      setUserInfo(u => ({ ...u, [`step${step}`]: text }));
      setMessages(m => [...m, { sender: 'bot', text: prompts[step - 1] }]);
      setStep(s => s + 1);
      return;
    }

    // After onboarding, send to backend
    postMessage(text);
  };

  const handleKey = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between bg-indigo-600 text-white p-3">
        <h2 className="text-lg font-medium">Travel Assistant</h2>
        <button onClick={onClose} className="text-2xl leading-none">×</button>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-3 space-y-2 bg-gray-50 dark:bg-gray-700"
      >
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-[75%] break-words
                ${m.sender === 'user'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white dark:bg-gray-600 text-gray-900 dark:text-gray-100'}`
            }
            >
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-center text-sm text-gray-500">Typing...</div>
        )}
      </div>

      {/* Input */}
      <div className="flex p-3 border-t border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800">
        <textarea
          className="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-indigo-400"
          rows={2}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Type your message…"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="ml-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
