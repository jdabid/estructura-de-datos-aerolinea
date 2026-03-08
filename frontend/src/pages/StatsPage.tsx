import { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import apiClient from '../api/client';

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

interface CandyStats {
  entries: string[];
  total_count: number;
}

const PIE_COLORS = ['#3b82f6', '#22c55e', '#a855f7', '#f97316'];

const CUSTOM_TOOLTIP_STYLE = {
  backgroundColor: '#1f2937',
  border: '1px solid #374151',
  borderRadius: '8px',
  color: '#d1d5db',
};

export default function StatsPage() {
  const [stats, setStats] = useState<GeneralStats | null>(null);
  const [destinations, setDestinations] = useState<PopularDestinations | null>(null);
  const [candy, setCandy] = useState<CandyStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [generalRes, destRes, candyRes] = await Promise.all([
          apiClient.get('/stats/general'),
          apiClient.get('/stats/destinations'),
          apiClient.get('/stats/candy'),
        ]);
        setStats(generalRes.data);
        setDestinations(destRes.data);
        setCandy(candyRes.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar estadisticas');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-700 rounded w-56"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-28 bg-gray-700 rounded-lg"></div>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="h-80 bg-gray-700 rounded-lg"></div>
            <div className="h-80 bg-gray-700 rounded-lg"></div>
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

  const summaryCards = [
    {
      title: 'Recaudo Total',
      value: `$${stats?.total_revenue?.toLocaleString() ?? '0'}`,
      color: 'from-green-500 to-emerald-600',
      dotColor: 'bg-green-400',
    },
    {
      title: 'Reservas con Mascotas',
      value: stats?.total_pet_bookings ?? 0,
      color: 'from-blue-500 to-cyan-600',
      dotColor: 'bg-blue-400',
    },
    {
      title: 'Infantes Registrados',
      value: stats?.total_infant_count ?? 0,
      color: 'from-purple-500 to-violet-600',
      dotColor: 'bg-purple-400',
    },
    {
      title: 'Costo Total Dulces',
      value: `$${stats?.total_candy_cost?.toLocaleString() ?? '0'}`,
      color: 'from-orange-500 to-amber-600',
      dotColor: 'bg-orange-400',
    },
  ];

  const pieData = [
    { name: 'Recaudo', value: stats?.total_revenue ?? 0 },
    { name: 'Mascotas', value: stats?.total_pet_bookings ?? 0 },
    { name: 'Infantes', value: stats?.total_infant_count ?? 0 },
    { name: 'Dulces', value: stats?.total_candy_cost ?? 0 },
  ].filter((d) => d.value > 0);

  const barData = destinations?.destinations ?? [];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Estadisticas</h1>
        <p className="text-gray-400">Visualizacion grafica del sistema de reservas</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryCards.map((card) => (
          <div
            key={card.title}
            className="bg-gray-800 border border-gray-700 rounded-lg p-5"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className={`w-2 h-2 rounded-full ${card.dotColor}`}></span>
              <p className="text-gray-400 text-sm">{card.title}</p>
            </div>
            <p className="text-2xl font-bold text-white">{card.value}</p>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bar Chart - Bookings por destino */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-white mb-1">Reservas por Destino</h2>
          {destinations?.most_popular && (
            <p className="text-sm text-blue-400 mb-4">
              Mas popular: {destinations.most_popular}
            </p>
          )}
          {barData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="destination"
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                  axisLine={{ stroke: '#4b5563' }}
                  tickLine={{ stroke: '#4b5563' }}
                />
                <YAxis
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                  axisLine={{ stroke: '#4b5563' }}
                  tickLine={{ stroke: '#4b5563' }}
                  allowDecimals={false}
                />
                <Tooltip
                  contentStyle={CUSTOM_TOOLTIP_STYLE}
                  labelStyle={{ color: '#f3f4f6' }}
                  cursor={{ fill: 'rgba(55, 65, 81, 0.5)' }}
                  formatter={(value: number) => [`${value} reservas`, 'Total']}
                />
                <Bar dataKey="total_bookings" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              No hay datos de destinos disponibles
            </div>
          )}
        </div>

        {/* Pie Chart - Distribucion de metricas */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-white mb-4">
            Distribucion de Metricas
          </h2>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={4}
                  dataKey="value"
                  stroke="none"
                >
                  {pieData.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={PIE_COLORS[index % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={CUSTOM_TOOLTIP_STYLE}
                  formatter={(value: number, name: string) => [
                    value.toLocaleString(),
                    name,
                  ]}
                />
                <Legend
                  wrapperStyle={{ color: '#d1d5db', fontSize: '13px' }}
                  iconType="circle"
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              No hay datos disponibles
            </div>
          )}
        </div>
      </div>

      {/* Candy Stats */}
      {candy && candy.total_count > 0 && (
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">
              Registro de Dulces para Infantes
            </h2>
            <span className="bg-orange-500/20 text-orange-400 px-3 py-1 rounded-full text-sm font-medium">
              {candy.total_count} entregas
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-64 overflow-y-auto">
            {candy.entries.map((entry, i) => (
              <div
                key={i}
                className="bg-gray-700/50 rounded-lg px-4 py-2 text-gray-300 text-sm"
              >
                {entry}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
