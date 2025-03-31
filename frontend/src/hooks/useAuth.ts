import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { auth as authService } from '../services/api';

interface User {
  id: number;
  email: string;
  username: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshAuth: () => Promise<boolean>;
}

export function useAuth(): AuthContextType {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    console.log('Checking auth status, token exists:', !!token);
    if (token) {
      try {
        // Verify token and get user info
        const response = await authService.getCurrentUser();
        console.log('Auth check successful, user data received');
        setUser(response.data);
        return true;
      } catch (error) {
        console.error('Auth check failed, clearing token', error);
        localStorage.removeItem('token');
        setUser(null);
        return false;
      }
    } else {
      console.log('No token found during auth check');
      setUser(null);
      return false;
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      await checkAuthStatus();
      setLoading(false);
    };
    
    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      const userData: User = response.data.user;
      setUser(userData);
      navigate('/');
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, username: string, password: string) => {
    try {
      const response = await authService.register(email, username, password);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      const userData: User = response.data.user;
      setUser(userData);
      navigate('/');
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/login');
  };

  return { user, loading, login, register, logout, refreshAuth: checkAuthStatus };
} 