import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import FlightCard from './FlightCard';

export default function ChatInterface({ siteId, mode, onModeChange, onClose }) {
  // Onboarding: 1=name, 2=phone, 3=email, 4=chat
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const sessionIdRef = useRef(crypto.randomUUID());
  const [loading, setLoading] = useState(false);
  const [offers, setOffers] = useState([]);
  const [showOffers, setShowOffers] = useState(false);
  const scrollRef = useRef(null);

  // For flight form UI
  const [flightForm, setFlightForm] = useState({
    origin: '',
    destination: '',
    departure_date: '',
    adults: 1
  });

  useEffect(() => {
    setMessages([{ sender: 'bot', text: 'Hello! What is your name?' }]);
  }, []);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, offers]);

  // Email validation utility (optional)
  const isValidEmail = (email) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text) return;

    setMessages(prev => [...prev, { sender: 'user', text }]);
    setInput('');

    if (step === 1) {
      setName(text);
      setMessages(prev => [...prev, { sender: 'bot', text: `Nice to meet you, ${text}! Could you share your phone number?` }]);
      setStep(2);
      return;
    }
    if (step === 2) {
      setPhone(text);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Great, and what is your email address?' }]);
      setStep(3);
      return;
    }
    if (step === 3) {
      setEmail(text);

      // OPTIONAL: Basic frontend validation (for UX)
      if (!isValidEmail(text)) {
        setMessages(prev => [
          ...prev,
          { sender: 'bot', text: '❌ Please enter a valid email address.' }
        ]);
        setStep(3);
        return;
      }

      // SEND LEAD TO BACKEND!
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/leads`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, phone, email: text })
        });

        if (!res.ok) {
          const data = await res.json();
          if (data.detail && Array.isArray(data.detail)) {
            const emailErr = data.detail.find(d =>
              d.loc && d.loc.includes('email')
            );
            if (emailErr) {
              setMessages(prev => [
                ...prev,
                { sender: 'bot', text: '❌ Please enter a valid email address.' }
              ]);
              setStep(3); // Stay on the same step!
              return;
            }
          }
          throw new Error('Lead capture failed');
        }
      } catch (err) {
        setMessages(prev => [
          ...prev,
          { sender: 'bot', text: 'Sorry, could not save your details. Try again.' }
        ]);
        setStep(3);
        return;
      }

      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: `Thanks, ${name}! We have your phone as ${phone} and email as ${text}. How can I assist you today?` }
      ]);
      setStep(4);
      return;
    }

    setLoading(true);

    if (mode === 'flight') {
      // The old (text-parse) logic is replaced by the form below!
      // The flight form now does its own submit.
      setLoading(false);
      return;
    } else {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/api/chat`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ site_id: siteId, session_id: sessionIdRef.current, message: text }),
          }
        );
        if (!res.ok) throw new Error('Chat service error');
        const { reply, session_id } = await res.json();
        sessionIdRef.current = session_id;
        setMessages(prev => [...prev, { sender: 'bot', text: reply }]);
      } catch {
        setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, something went wrong.' }]);
      }
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Flight search form submit
  const handleFlightFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowOffers(false);

    const { origin, destination, departure_date, adults } = flightForm;

    if (!origin || !destination || !departure_date) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Please fill all fields.' }]);
      setLoading(false);
      return;
    }
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/api/flights/search`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ origin, destination, departure_date, return_date: null, adults }),
        }
      );
      if (!res.ok) throw new Error('Flight search failed');
      const data = await res.json();
      setOffers(data);
      setShowOffers(true);
      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: `Here are flights from ${origin} to ${destination}:` }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: 'Sorry, I could not fetch flights right now.' }
      ]);
    }
    setLoading(false);
    onModeChange('chat');
  };

  return (
    <div className="chat-interface flex flex-col h-full bg-white dark:bg-gray-800 rounded-t-lg">
      <div className="sticky top-0 z-10 bg-indigo-600 text-white px-4 py-2 font-medium flex justify-between items-center">
        <span>Chat with us</span>
        {onClose && <button onClick={onClose}>✕</button>}
      </div>

      <div ref={scrollRef} className="chat-messages flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`message flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`bubble max-w-[75%] px-4 py-2 rounded-lg shadow-md whitespace-pre-wrap break-words ${m.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-900'
              }`}>
              <div className="prose prose-sm dark:prose-invert">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.text}</ReactMarkdown>
              </div>
            </div>
          </div>
        ))}

        {showOffers && (
          <div className="overflow-x-auto flex space-x-4 py-4">
            {offers.map(o => (
              <FlightCard key={o.id} offer={o} onSelect={() => setMessages(prev => [...prev, { sender: 'user', text: `BOOK:${o.id}` }])} />
            ))}
          </div>
        )}

        {loading && <div className="text-center text-gray-500">Typing…</div>}
      </div>

      <div className="chat-input-container flex items-center p-4 border-t border-gray-300 bg-gray-100 dark:bg-gray-700">
        {mode === 'flight' ? (
          <form
            className="flex flex-col gap-2 w-full"
            onSubmit={handleFlightFormSubmit}
          >
            <div className="flex gap-2">
              <input
                name="origin"
                placeholder="From (DEL)"
                className="flex-1 p-2 border rounded"
                value={flightForm.origin}
                onChange={e => setFlightForm(f => ({ ...f, origin: e.target.value.toUpperCase() }))}
              />
              <input
                name="destination"
                placeholder="To (LHR)"
                className="flex-1 p-2 border rounded"
                value={flightForm.destination}
                onChange={e => setFlightForm(f => ({ ...f, destination: e.target.value.toUpperCase() }))}
              />
            </div>
            <div className="flex gap-2 mt-1">
              <input
                name="departure_date"
                type="date"
                className="flex-1 p-2 border rounded"
                value={flightForm.departure_date}
                onChange={e => setFlightForm(f => ({ ...f, departure_date: e.target.value }))}
              />
              <input
                name="adults"
                type="number"
                min="1"
                value={flightForm.adults}
                className="w-24 p-2 border rounded"
                onChange={e => setFlightForm(f => ({ ...f, adults: Number(e.target.value) }))}
                placeholder="Adults"
              />
            </div>
            <button
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg mt-2 disabled:opacity-50"
              disabled={loading}
              type="submit"
            >
              {loading ? 'Searching...' : 'Search Flights'}
            </button>
          </form>
        ) : (
          <textarea
            className="chat-input flex-1 border border-gray-300 rounded-lg p-2 mr-2 resize-none"
            rows={2}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
          />
        )}
        {mode !== 'flight' && (
          <button
            className="send-button bg-indigo-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            {loading ? '...' : 'Send'}
          </button>
        )}
      </div>
    </div>
  );
}
