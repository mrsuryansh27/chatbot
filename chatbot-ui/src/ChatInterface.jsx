import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatInterface({ siteId }) {
  // Onboarding: 1=name, 2=phone, 3=email, 4=chat
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId] = useState(() => crypto.randomUUID());
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    setMessages([{ sender: 'bot', text: 'Hello! What is your name?' }]);
  }, []);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text) return;
    setMessages(prev => [...prev, { sender: 'user', text }]);
    setInput('');

    // Onboarding steps
    if (step === 1) {
      setName(text);
      setMessages(prev => [...prev,
      { sender: 'bot', text: `Nice to meet you, ${text}! Could you share your phone number?` }
      ]);
      setStep(2);
      return;
    }
    if (step === 2) {
      setPhone(text);
      setMessages(prev => [...prev,
      { sender: 'bot', text: 'Great, and what is your email address?' }
      ]);
      setStep(3);
      return;
    }
    if (step === 3) {
      setEmail(text);
      setMessages(prev => [...prev,
      { sender: 'bot', text: `Thanks, ${name}! We have your phone as ${phone} and email as ${text}. How can I assist you today?`, isCTA: true }
      ]);
      setStep(4);
      return;
    }

    // Backend chat
    setLoading(true);
    try {
      const res = await fetch(import.meta.env.VITE_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          site_id: siteId,
          message: text,
          history: messages.map(m => ({ role: m.sender === 'bot' ? 'assistant' : 'user', content: m.text }))
        })
      });
      const { reply } = await res.json();
      setMessages(prev => [...prev,
      { sender: 'bot', text: reply }
      ]);
    } catch {
      setMessages(prev => [...prev,
      { sender: 'bot', text: 'Oops, something went wrong.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-interface flex flex-col h-full">
      {/* <div className="chat-header">Chat with us</div> */}
      <div className="bg-indigo-600 text-white px-4 py-2 rounded-t-lg font-medium">
        Chat with us
      </div>
      <div ref={scrollRef} className="chat-messages flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`message flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className={`bubble max-w-[75%] px-4 py-2 rounded-lg shadow-md whitespace-pre-wrap break-words ${m.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-900'
              }`}>
              <div className="prose prose-sm dark:prose-invert">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {m.text}
                </ReactMarkdown>
              </div>
            </div>
            {m.isCTA && (
              <button
                className="mt-2 px-4 py-2 bg-green-500 text-white rounded self-start"
                onClick={() => window.location.href = 'tel:+1234567890'}
              >
                Call for Offers
              </button>
            )}
          </div>
        ))}
      </div>
      <div className="chat-input-container flex items-center p-4 border-t border-gray-300">
        <textarea
          className="chat-input flex-1 border border-gray-300 rounded-lg p-2 mr-2"
          rows={2}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <button
          className="send-button bg-indigo-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
          onClick={sendMessage}
          disabled={loading || !input.trim()}
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
