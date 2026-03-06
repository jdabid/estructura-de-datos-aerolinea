import { useEffect, useState } from 'react';
import apiClient from '../api/client';
import { useAuthStore } from '../stores/authStore';

interface GeneralStats {
  total_revenue: number;
  total_pet_bookings: number;
  total_infant_count: number;
  total_candy_cost: number;
}

interface DestinationStat {
  destination: string;
  total_bookings: number;
}

interface PopularDestinations {
  destinations: DestinationStat[];
  most_popular: string | null;
}

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<GeneralStats | null>(null);
  const [destinations, setDestinations] = useState<PopularDestinations | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [generalRes, destRes] = await Promise.all([
          apiClient.get('/stats/general'),
          apiClient.get('/stats/destinations'),
        ]);
        setStats(generalRes.data);
        setDestinations(destRes.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar estadisticas');
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-48"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
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

  const statCards = [
    {
      title: 'Recaudo Total',
      value: `$${stats?.total_revenue?.toLocaleString() ?? '0'}`,
      icon: '💰',
      color: 'from-green-500 to-emerald-600',
    },
    {
      title: 'Reservas con Mascotas',
      value: stats?.total_pet_bookings ?? 0,
      icon: '🐾',
      color: 'from-blue-500 to-cyan-600',
    },
    {
      title: 'Infantes Registrados',
      value: stats?.total_infant_count ?? 0,
      icon: '👶',
      color: 'from-purple-500 to-violet-600',
    },
    {
      title: 'Costo Total Dulces',
      value: `$${stats?.total_candy_cost?.toLocaleString() ?? '0'}`,
      icon: '🍬',
      color: 'from-orange-500 to-amber-600',
    },
  ];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400">Bienvenido, {user?.full_name}</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((card) => (
          <div
            key={card.title}
            className={`bg-gradient-to-br ${card.color} rounded-lg p-6 shadow-lg`}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-white/80 text-sm">{card.title}</p>
                <p className="text-2xl font-bold text-white mt-1">{card.value}</p>
              </div>
              <span className="text-3xl">{card.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Popular Destinations */}
      {destinations && (
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white mb-4">
            Destinos Populares
            {destinations.most_popular && (
              <span className="ml-2 text-sm font-normal text-blue-400">
                Mas popular: {destinations.most_popular}
              </span>
            )}
          </h2>
          {destinations.destinations.length > 0 ? (
            <div className="space-y-3">
              {destinations.destinations.map((dest) => (
                <div
                  key={dest.destination}
                  className="flex items-center justify-between bg-gray-700/50 rounded-lg px-4 py-3"
                >
                  <span className="text-white font-medium">{dest.destination}</span>
                  <span className="text-gray-300 bg-gray-600 px-3 py-1 rounded-full text-sm">
                    {dest.total_bookings} reservas
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400">No hay datos de destinos disponibles.</p>
          )}
        </div>
      )}
    </div>
  );
}
