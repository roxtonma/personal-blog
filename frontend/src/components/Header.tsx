import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import LoginModal from './LoginModal';

interface HeaderProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

const Header = ({ currentPage, onNavigate }: HeaderProps): React.ReactElement => {
  const { isAuthenticated, login, logout, loading } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleWriteClick = () => {
    if (isAuthenticated) {
      onNavigate('editor');
    } else {
      setShowLoginModal(true);
    }
  };

  const handleLogin = async (password: string) => {
    const success = await login(password);
    if (success) {
      onNavigate('editor');
    }
    return success;
  };

  if (loading) {
    return (
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
        </div>
      </header>
    );
  }

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Roxton's Blog</h1>
              </div>
              <nav className="flex space-x-6">
                <button
                  onClick={() => onNavigate('home')}
                  className={`px-3 py-2 text-sm font-medium rounded-md transition ${
                    currentPage === 'home'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Posts
                </button>
                <button
                  onClick={handleWriteClick}
                  className={`px-3 py-2 text-sm font-medium rounded-md transition ${
                    currentPage === 'editor'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  {isAuthenticated ? 'Write' : 'Write (Login)'}
                </button>
              </nav>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                {new Date().toLocaleDateString('en-US', { 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </div>
              
              {isAuthenticated && (
                <div className="flex items-center space-x-3">
                  <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
                    Admin
                  </span>
                  <button
                    onClick={logout}
                    className="text-sm text-gray-600 hover:text-gray-900 px-2 py-1 rounded transition"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLogin={handleLogin}
      />
    </>
  );
};

export default Header;