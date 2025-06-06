import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '@/api/axios';
import { useAuth } from '@/context/AuthContext';

function LoginPage() {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState(null);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const { data } = await api.post('/auth/token/', credentials);
      login(data.access);
      if (data.refresh) {
        localStorage.setItem('refresh', data.refresh);
      }
      navigate('/projects');
    } catch (err) {
      setError('نام کاربری یا رمز عبور اشتباه است');
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <h2 className="mb-4 text-center">ورود</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">نام کاربری</label>
          <input type="text" name="username" className="form-control" value={credentials.username} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">رمز عبور</label>
          <input type="password" name="password" className="form-control" value={credentials.password} onChange={handleChange} required />
        </div>
        <button className="btn btn-primary w-100" type="submit">ورود</button>
      </form>
      <p className="mt-3 text-center">
        حساب ندارید؟ <Link to="/register">ثبت‌نام</Link>
      </p>
    </div>
  );
}

export default LoginPage; 