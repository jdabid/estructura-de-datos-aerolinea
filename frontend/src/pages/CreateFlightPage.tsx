import { useEffect, useState } from 'react';
import apiClient from '../api/client';

interface Destination {
  id: number;
  name: string;
  tax_amount: number;
  is_promotion: boolean;
  allows_pets: boolean;
}

export default function CreateFlightPage() {
  const [destinations, setDestinations] = useState<Destination[]>([]);

  // Destination form
  const [destName, setDestName] = useState('');
  const [taxAmount, setTaxAmount] = useState('');
  const [isPromotion, setIsPromotion] = useState(false);
  const [allowsPets, setAllowsPets] = useState(true);
  const [destLoading, setDestLoading] = useState(false);
  const [destSuccess, setDestSuccess] = useState<string | null>(null);
  const [destError, setDestError] = useState<string | null>(null);

  // Flight form
  const [flightNumber, setFlightNumber] = useState('');
  const [origin, setOrigin] = useState('');
  const [basePrice, setBasePrice] = useState('');
  const [destinationId, setDestinationId] = useState('');
  const [flightLoading, setFlightLoading] = useState(false);
  const [flightSuccess, setFlightSuccess] = useState<string | null>(null);
  const [flightError, setFlightError] = useState<string | null>(null);

  const fetchDestinations = async () => {
    try {
      const res = await apiClient.get('/flights/destinations/');
      setDestinations(res.data);
    } catch {
      // silent
    }
  };

  useEffect(() => {
    fetchDestinations();
  }, []);

  const handleCreateDestination = async (e: React.FormEvent) => {
    e.preventDefault();
    setDestLoading(true);
    setDestError(null);
    setDestSuccess(null);
    try {
      const res = await apiClient.post('/flights/destinations/', {
        name: destName,
        tax_amount: parseFloat(taxAmount),
        is_promotion: isPromotion,
        allows_pets: allowsPets,
      });
      setDestSuccess(`Destino "${res.data.name}" creado exitosamente`);
      setDestName('');
      setTaxAmount('');
      setIsPromotion(false);
      setAllowsPets(true);
      fetchDestinations();
    } catch (err: any) {
      setDestError(err.response?.data?.detail || 'Error al crear destino');
    } finally {
      setDestLoading(false);
    }
  };

  const handleCreateFlight = async (e: React.FormEvent) => {
    e.preventDefault();
    setFlightLoading(true);
    setFlightError(null);
    setFlightSuccess(null);
    try {
      const res = await apiClient.post('/flights/', {
        flight_number: flightNumber,
        origin,
        base_price: parseFloat(basePrice),
        destination_id: parseInt(destinationId),
      });
      setFlightSuccess(`Vuelo "${res.data.flight_number}" creado exitosamente`);
      setFlightNumber('');
      setOrigin('');
      setBasePrice('');
      setDestinationId('');
    } catch (err: any) {
      setFlightError(err.response?.data?.detail || 'Error al crear vuelo');
    } finally {
      setFlightLoading(false);
    }
  };

  const inputClass =
    'w-full bg-gray-700 text-white rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500';
  const labelClass = 'block text-sm font-medium text-gray-300 mb-1';

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Crear Destino y Vuelo</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Crear Destino */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white mb-4">Nuevo Destino</h2>

          {destSuccess && (
            <div className="bg-green-500/20 border border-green-500 text-green-300 px-4 py-3 rounded mb-4">
              {destSuccess}
            </div>
          )}
          {destError && (
            <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded mb-4">
              {destError}
            </div>
          )}

          <form onSubmit={handleCreateDestination} className="space-y-4">
            <div>
              <label className={labelClass}>Nombre del destino</label>
              <input
                type="text"
                value={destName}
                onChange={(e) => setDestName(e.target.value)}
                className={inputClass}
                required
              />
            </div>
            <div>
              <label className={labelClass}>Impuesto</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={taxAmount}
                onChange={(e) => setTaxAmount(e.target.value)}
                className={inputClass}
                required
              />
            </div>
            <div className="flex items-center gap-6">
              <label className="flex items-center gap-2 text-gray-300">
                <input
                  type="checkbox"
                  checked={isPromotion}
                  onChange={(e) => setIsPromotion(e.target.checked)}
                  className="rounded bg-gray-700 border-gray-600"
                />
                Promocion (-10%)
              </label>
              <label className="flex items-center gap-2 text-gray-300">
                <input
                  type="checkbox"
                  checked={allowsPets}
                  onChange={(e) => setAllowsPets(e.target.checked)}
                  className="rounded bg-gray-700 border-gray-600"
                />
                Permite mascotas
              </label>
            </div>
            <button
              type="submit"
              disabled={destLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition disabled:opacity-50"
            >
              {destLoading ? 'Creando...' : 'Crear Destino'}
            </button>
          </form>
        </div>

        {/* Crear Vuelo */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white mb-4">Nuevo Vuelo</h2>

          {flightSuccess && (
            <div className="bg-green-500/20 border border-green-500 text-green-300 px-4 py-3 rounded mb-4">
              {flightSuccess}
            </div>
          )}
          {flightError && (
            <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded mb-4">
              {flightError}
            </div>
          )}

          <form onSubmit={handleCreateFlight} className="space-y-4">
            <div>
              <label className={labelClass}>Numero de vuelo</label>
              <input
                type="text"
                value={flightNumber}
                onChange={(e) => setFlightNumber(e.target.value)}
                className={inputClass}
                placeholder="AV-001"
                required
              />
            </div>
            <div>
              <label className={labelClass}>Origen</label>
              <input
                type="text"
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
                className={inputClass}
                placeholder="Bogota"
                required
              />
            </div>
            <div>
              <label className={labelClass}>Precio base</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={basePrice}
                onChange={(e) => setBasePrice(e.target.value)}
                className={inputClass}
                required
              />
            </div>
            <div>
              <label className={labelClass}>Destino</label>
              <select
                value={destinationId}
                onChange={(e) => setDestinationId(e.target.value)}
                className={inputClass}
                required
              >
                <option value="">Seleccionar destino</option>
                {destinations.map((dest) => (
                  <option key={dest.id} value={dest.id}>
                    {dest.name} (Impuesto: ${dest.tax_amount})
                  </option>
                ))}
              </select>
            </div>
            <button
              type="submit"
              disabled={flightLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition disabled:opacity-50"
            >
              {flightLoading ? 'Creando...' : 'Crear Vuelo'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
