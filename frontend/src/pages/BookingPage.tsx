import { useEffect, useMemo, useState } from 'react';
import apiClient from '../api/client';

interface Destination {
  id: number;
  name: string;
  tax_amount: number;
  is_promotion: boolean;
  allows_pets: boolean;
}

interface Flight {
  id: number;
  flight_number: string;
  origin: string;
  base_price: number;
  destination_id: number;
  destination: Destination;
}

interface BookingResult {
  id: number;
  passenger_name: string;
  passenger_age: number;
  has_pet: boolean;
  flight_id: number;
  total_price: number;
  created_at: string;
}

export default function BookingPage() {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loadingFlights, setLoadingFlights] = useState(true);

  // Form state
  const [selectedFlightId, setSelectedFlightId] = useState('');
  const [passengerName, setPassengerName] = useState('');
  const [passengerAge, setPassengerAge] = useState('');
  const [hasPet, setHasPet] = useState(false);

  // Submit state
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [bookingResult, setBookingResult] = useState<BookingResult | null>(null);

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        const res = await apiClient.get('/flights/');
        setFlights(res.data);
      } catch {
        setError('Error al cargar vuelos');
      } finally {
        setLoadingFlights(false);
      }
    };
    fetchFlights();
  }, []);

  const selectedFlight = useMemo(
    () => flights.find((f) => f.id === parseInt(selectedFlightId)),
    [flights, selectedFlightId]
  );

  const age = parseInt(passengerAge) || 0;
  const isInfant = age > 0 && age < 12;
  const petBlocked = hasPet && selectedFlight && !selectedFlight.destination.allows_pets;

  const priceBreakdown = useMemo(() => {
    if (!selectedFlight) return null;
    const { base_price, destination } = selectedFlight;
    const hasPromo = destination.is_promotion;
    const discountedPrice = hasPromo ? base_price * 0.9 : base_price;
    const total = discountedPrice + destination.tax_amount;
    return {
      basePrice: base_price,
      hasPromo,
      discount: hasPromo ? base_price * 0.1 : 0,
      discountedPrice,
      tax: destination.tax_amount,
      total,
    };
  }, [selectedFlight]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (petBlocked) return;
    setSubmitting(true);
    setError(null);
    setBookingResult(null);
    try {
      const res = await apiClient.post('/bookings/', {
        passenger_name: passengerName,
        passenger_age: age,
        has_pet: hasPet,
        flight_id: parseInt(selectedFlightId),
      });
      setBookingResult(res.data);
      setPassengerName('');
      setPassengerAge('');
      setHasPet(false);
      setSelectedFlightId('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear reserva');
    } finally {
      setSubmitting(false);
    }
  };

  const inputClass =
    'w-full bg-gray-700 text-white rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500';
  const labelClass = 'block text-sm font-medium text-gray-300 mb-1';

  if (loadingFlights) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-48"></div>
          <div className="h-64 bg-gray-700 rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Nueva Reserva</h1>

      {bookingResult && (
        <div className="bg-green-500/20 border border-green-500 text-green-300 px-4 py-4 rounded-lg mb-6">
          <p className="font-semibold mb-1">Reserva creada exitosamente</p>
          <p className="text-sm">
            ID: {bookingResult.id} — Pasajero: {bookingResult.passenger_name} — Total: $
            {bookingResult.total_price.toFixed(2)}
          </p>
        </div>
      )}

      {error && (
        <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Formulario */}
        <div className="lg:col-span-2 bg-gray-800 rounded-lg p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white mb-4">Datos de la Reserva</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className={labelClass}>Vuelo</label>
              <select
                value={selectedFlightId}
                onChange={(e) => setSelectedFlightId(e.target.value)}
                className={inputClass}
                required
              >
                <option value="">Seleccionar vuelo</option>
                {flights.map((f) => (
                  <option key={f.id} value={f.id}>
                    {f.flight_number} — {f.origin} → {f.destination.name} (${f.base_price.toFixed(2)})
                  </option>
                ))}
              </select>
            </div>

            {selectedFlight && (
              <div className="bg-gray-700/50 rounded-lg p-3 text-sm text-gray-300">
                <span className="font-medium text-white">{selectedFlight.flight_number}</span>
                {' · '}
                {selectedFlight.origin} → {selectedFlight.destination.name}
                {selectedFlight.destination.is_promotion && (
                  <span className="ml-2 bg-green-500/20 text-green-400 text-xs px-2 py-0.5 rounded-full">
                    Promo -10%
                  </span>
                )}
                {!selectedFlight.destination.allows_pets && (
                  <span className="ml-2 bg-red-500/20 text-red-400 text-xs px-2 py-0.5 rounded-full">
                    Sin mascotas
                  </span>
                )}
              </div>
            )}

            <div>
              <label className={labelClass}>Nombre del pasajero</label>
              <input
                type="text"
                value={passengerName}
                onChange={(e) => setPassengerName(e.target.value)}
                className={inputClass}
                required
              />
            </div>

            <div>
              <label className={labelClass}>Edad</label>
              <input
                type="number"
                min="0"
                max="150"
                value={passengerAge}
                onChange={(e) => setPassengerAge(e.target.value)}
                className={inputClass}
                required
              />
              {isInfant && (
                <p className="mt-1 text-sm text-purple-400">
                  Infante detectado — se registrara costo de dulce ($5.00)
                </p>
              )}
            </div>

            <div>
              <label className="flex items-center gap-2 text-gray-300">
                <input
                  type="checkbox"
                  checked={hasPet}
                  onChange={(e) => setHasPet(e.target.checked)}
                  className="rounded bg-gray-700 border-gray-600"
                />
                Viaja con mascota
              </label>
              {petBlocked && (
                <p className="mt-1 text-sm text-red-400">
                  El destino {selectedFlight?.destination.name} no permite mascotas
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={submitting || !!petBlocked}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded transition disabled:opacity-50"
            >
              {submitting ? 'Creando reserva...' : 'Confirmar Reserva'}
            </button>
          </form>
        </div>

        {/* Panel de precio en tiempo real */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg h-fit">
          <h2 className="text-lg font-semibold text-white mb-4">Desglose de Precio</h2>
          {priceBreakdown ? (
            <div className="space-y-3">
              <div className="flex justify-between text-gray-300">
                <span>Precio base</span>
                <span className="text-white">${priceBreakdown.basePrice.toFixed(2)}</span>
              </div>

              {priceBreakdown.hasPromo && (
                <div className="flex justify-between text-green-400">
                  <span>Descuento promo (-10%)</span>
                  <span>-${priceBreakdown.discount.toFixed(2)}</span>
                </div>
              )}

              <div className="flex justify-between text-gray-300">
                <span>Impuesto</span>
                <span className="text-white">+${priceBreakdown.tax.toFixed(2)}</span>
              </div>

              <div className="border-t border-gray-700 pt-3 flex justify-between">
                <span className="text-lg font-bold text-white">Total</span>
                <span className="text-lg font-bold text-blue-400">
                  ${priceBreakdown.total.toFixed(2)}
                </span>
              </div>

              {isInfant && (
                <div className="bg-purple-500/20 border border-purple-500/30 rounded p-3 mt-2">
                  <p className="text-purple-300 text-sm">
                    Costo dulce infante: $5.00 (registrado en sistema)
                  </p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">Selecciona un vuelo para ver el desglose</p>
          )}
        </div>
      </div>
    </div>
  );
}
