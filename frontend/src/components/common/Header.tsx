import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Header: React.FC = () => {
  const location = useLocation();

  const navLinks = [
    { path: '/', label: 'Dashboard' },
    { path: '/rankings', label: 'Classifiche' },
  ];

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <span className="text-3xl">🚴</span>
            <h1 className="text-2xl font-bold text-gray-800">PCS Assistant</h1>
          </Link>

          <nav className="flex items-center gap-6">
            {navLinks.map(link => (
              <Link
                key={link.path}
                to={link.path}
                className={`text-sm font-medium transition-colors ${
                  location.pathname === link.path
                    ? 'text-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};
