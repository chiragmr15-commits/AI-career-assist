import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './services/store';
import { Navbar } from './components/Navbar';
import { Auth } from './components/Auth';
import { Dashboard } from './components/Dashboard';
import { ResumeAnalyzer } from './components/ResumeAnalyzer';
import { CareerRecommendation } from './components/CareerRecommendation';
import { InterviewSimulator } from './components/InterviewSimulator';
import { EmotionTracker } from './components/EmotionTracker';
import './styles/globals.css';

function App() {
  const { isAuthenticated, logout } = useAuthStore();
  const [isAuthenticatedState, setIsAuthenticatedState] = React.useState(isAuthenticated);

  React.useEffect(() => {
    setIsAuthenticatedState(isAuthenticated);
  }, [isAuthenticated]);

  return (
    <Router>
      {isAuthenticatedState ? (
        <div className="min-h-screen bg-dark-900">
          <Navbar onLogout={() => {
            logout();
            setIsAuthenticatedState(false);
          }} />
          <div className="max-w-7xl mx-auto px-4 py-8">
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/resume" element={<ResumeAnalyzer />} />
              <Route path="/career" element={<CareerRecommendation />} />
              <Route path="/interview" element={<InterviewSimulator />} />
              <Route path="/emotion" element={<EmotionTracker />} />
              <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
          </div>
        </div>
      ) : (
        <Auth onSuccess={() => setIsAuthenticatedState(true)} />
      )}
    </Router>
  );
}

export default App;
