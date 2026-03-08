import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useAuthStore } from './stores/authStore';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import FlightsPage from './pages/FlightsPage';
import CreateFlightPage from './pages/CreateFlightPage';
import BookingPage from './pages/BookingPage';
import BookingsPage from './pages/BookingsPage';
import StatsPage from './pages/StatsPage';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

function App() {
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<DashboardPage />} />
          <Route path="/flights" element={<FlightsPage />} />
          <Route path="/create-flight" element={<CreateFlightPage />} />
          <Route path="/booking" element={<BookingPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
          <Route path="/stats" element={<StatsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
