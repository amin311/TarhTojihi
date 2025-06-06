import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '@/api/axios';

function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState(null);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await api.post('/users/register/', form);
      alert('ثبت‌نام موفق! اکنون وارد شوید.');
      navigate('/login');
    } catch (err) {
      setError('خطا در ثبت‌نام.');
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <h2 className="mb-4 text-center">ثبت‌نام</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">نام کاربری</label>
          <input className="form-control" name="username" value={form.username} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">ایمیل</label>
          <input className="form-control" name="email" type="email" value={form.email} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">رمز عبور</label>
          <input className="form-control" name="password" type="password" value={form.password} onChange={handleChange} required />
        </div>
        <button className="btn btn-primary w-100" type="submit">ثبت‌نام</button>
      </form>
      <p className="mt-3 text-center">
        حساب دارید؟ <Link to="/login">ورود</Link>
      </p>
    </div>
  );
}

export default RegisterPage; 