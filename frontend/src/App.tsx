import { useState } from 'react';
import './App.css';
import Body from './components/Body';
import Header from './components/Header';
import BlogEditor from './components/BlogEditor';
import { AuthProvider } from './components/AuthContext';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handlePostCreated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
  };

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        {currentPage === 'editor' ? (
          <BlogEditor onPostCreated={handlePostCreated} onNavigate={handleNavigate} />
        ) : (
          <>
            <Header currentPage={currentPage} onNavigate={handleNavigate} />
            <main>
              <Body refreshTrigger={refreshTrigger} />
            </main>
          </>
        )}
      </div>
    </AuthProvider>
  );
}

export default App;