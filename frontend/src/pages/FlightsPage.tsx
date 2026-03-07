import { useEffect, useState } from 'react';
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

export default function FlightsPage() {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [destRes, flightsRes] = await Promise.all([
          apiClient.get('/flights/destinations/'),
          apiClient.get('/flights/'),
        ]);
        setDestinations(destRes.data);
        setFlights(flightsRes.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar datos');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-48"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-700 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Destinos */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white mb-4">Destinos</h1>
        {destinations.length === 0 ? (
          <p className="text-gray-400">No hay destinos registrados.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {destinations.map((dest) => (
              <div key={dest.id} className="bg-gray-800 rounded-lg p-5 shadow-lg">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-semibold text-white">{dest.name}</h3>
                  <div className="flex gap-2">
                    {dest.is_promotion && (
                      <span className="bg-green-500/20 text-green-400 text-xs px-2 py-1 rounded-full">
                        Promo -10%
                      </span>
                    )}
                    {dest.allows_pets ? (
                      <span className="bg-blue-500/20 text-blue-400 text-xs px-2 py-1 rounded-full">
                        Mascotas OK
                      </span>
                    ) : (
                      <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded-full">
                        Sin mascotas
                      </span>
                    )}
                  </div>
                </div>
                <p className="text-gray-400 text-sm">
                  Impuesto: <span className="text-white font-medium">${dest.tax_amount.toFixed(2)}</span>
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Vuelos */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-4">Vuelos Disponibles</h2>
        {flights.length === 0 ? (
          <p className="text-gray-400">No hay vuelos disponibles.</p>
        ) : (
          <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-400">Vuelo</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-400">Origen</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-400">Destino</th>
                  <th className="text-right px-6 py-3 text-sm font-medium text-gray-400">Precio Base</th>
                  <th className="text-right px-6 py-3 text-sm font-medium text-gray-400">Impuesto</th>
                  <th className="text-center px-6 py-3 text-sm font-medium text-gray-400">Promo</th>
                </tr>
              </thead>
              <tbody>
                {flights.map((flight) => (
                  <tr key={flight.id} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                    <td className="px-6 py-4 text-white font-medium">{flight.flight_number}</td>
                    <td className="px-6 py-4 text-gray-300">{flight.origin}</td>
                    <td className="px-6 py-4 text-gray-300">{flight.destination.name}</td>
                    <td className="px-6 py-4 text-white text-right">${flight.base_price.toFixed(2)}</td>
                    <td className="px-6 py-4 text-gray-300 text-right">${flight.destination.tax_amount.toFixed(2)}</td>
                    <td className="px-6 py-4 text-center">
                      {flight.destination.is_promotion && (
                        <span className="bg-green-500/20 text-green-400 text-xs px-2 py-1 rounded-full">
                          -10%
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
