// src/FlightCard.jsx
export default function FlightCard({ offer, onSelect }) {
  return (
    <div className="min-w-[200px] p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
      <div className="font-semibold">
        {offer.departure_airport} → {offer.arrival_airport}
      </div>
      <div className="text-sm text-gray-600">
        {new Date(offer.departure_time).toLocaleTimeString()} –{' '}
        {new Date(offer.arrival_time).toLocaleTimeString()}
      </div>
      <div className="text-lg font-bold mt-auto">
        {offer.currency} {offer.total_amount}
      </div>
      <button
        className="mt-2 bg-indigo-600 text-white px-3 py-1 rounded"
        onClick={() => onSelect(offer.id)}
      >
        Book now
      </button>
    </div>
  );
}
