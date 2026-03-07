import { useEffect, useState } from 'react';
import apiClient from '../api/client';

interface Booking {
  id: number;
  passenger_name: string;
  passenger_age: number;
  has_pet: boolean;
  flight_id: number;
  total_price: number;
  created_at: string;
}

export default function BookingsPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const res = await apiClient.get('/bookings/');
        setBookings(res.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar reservas');
      } finally {
        setLoading(false);
      }
    };
    fetchBookings();
  }, []);

  const filtered = bookings.filter((b) =>
    b.passenger_name.toLowerCase().includes(search.toLowerCase())
  );

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-48"></div>
          <div className="h-10 bg-gray-700 rounded w-64"></div>
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-12 bg-gray-700 rounded"></div>
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
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">Historial de Reservas</h1>
        <span className="text-gray-400 text-sm">{bookings.length} reservas</span>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Buscar por nombre de pasajero..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-gray-800 text-white rounded px-4 py-2 w-full max-w-sm focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-700"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="bg-gray-800 rounded-lg p-8 text-center">
          <p className="text-gray-400">
            {search ? 'No se encontraron reservas para esa busqueda.' : 'No hay reservas registradas.'}
          </p>
        </div>
      ) : (
        <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-400">ID</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-400">Pasajero</th>
                <th className="text-center px-6 py-3 text-sm font-medium text-gray-400">Edad</th>
                <th className="text-center px-6 py-3 text-sm font-medium text-gray-400">Mascota</th>
                <th className="text-center px-6 py-3 text-sm font-medium text-gray-400">Vuelo</th>
                <th className="text-right px-6 py-3 text-sm font-medium text-gray-400">Precio Total</th>
                <th className="text-right px-6 py-3 text-sm font-medium text-gray-400">Fecha</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((booking) => (
                <tr key={booking.id} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                  <td className="px-6 py-4 text-gray-400 text-sm">#{booking.id}</td>
                  <td className="px-6 py-4 text-white font-medium">{booking.passenger_name}</td>
                  <td className="px-6 py-4 text-center">
                    <span className="text-gray-300">{booking.passenger_age}</span>
                    {booking.passenger_age < 12 && (
                      <span className="ml-2 bg-purple-500/20 text-purple-400 text-xs px-2 py-0.5 rounded-full">
                        Infante
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-center">
                    {booking.has_pet ? (
                      <span className="bg-blue-500/20 text-blue-400 text-xs px-2 py-1 rounded-full">
                        Si
                      </span>
                    ) : (
                      <span className="text-gray-500 text-sm">No</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-center text-gray-300">#{booking.flight_id}</td>
                  <td className="px-6 py-4 text-right text-white font-medium">
                    ${booking.total_price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-right text-gray-400 text-sm">
                    {formatDate(booking.created_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
