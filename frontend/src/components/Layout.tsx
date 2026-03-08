import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/flights', label: 'Vuelos' },
  { path: '/create-flight', label: 'Crear Vuelo' },
  { path: '/booking', label: 'Reservar' },
  { path: '/bookings', label: 'Reservas' },
  { path: '/stats', label: 'Estadisticas' },
];

export default function Layout() {
  const location = useLocation();
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-gray-900 flex">
      <aside className="w-64 bg-gray-800 border-r border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-lg font-bold text-white">Flight System</h2>
        </div>
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`block px-4 py-2 rounded transition ${
                location.pathname === item.path
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-0 w-64 p-4 border-t border-gray-700">
          <p className="text-sm text-gray-400 truncate">{user?.email}</p>
          <button
            onClick={logout}
            className="mt-2 text-sm text-red-400 hover:text-red-300"
          >
            Cerrar Sesion
          </button>
        </div>
      </aside>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}
