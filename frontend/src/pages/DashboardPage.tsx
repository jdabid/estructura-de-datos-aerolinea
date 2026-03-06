import { useAuthStore } from '../stores/authStore';

export default function DashboardPage() {
  const { user, logout } = useAuthStore();

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-300">{user?.full_name}</span>
          <button
            onClick={logout}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            Cerrar Sesion
          </button>
        </div>
      </div>
      <p className="text-gray-400">Bienvenido al sistema de reservas de vuelos.</p>
    </div>
  );
}
