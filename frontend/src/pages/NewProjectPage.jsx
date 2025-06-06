import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '@/api/axios';
import { useAuth } from '@/context/AuthContext';

function NewProjectPage() {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [form, setForm] = useState({ title: '', description: '', business_type: '' });
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [token, navigate]);

  const { data: categories = [], isLoading: loadingCats } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const { data } = await api.get('/categories/api/categories/');
      return data;
    },
  });

  const mutation = useMutation({
    mutationFn: async () => {
      const payload = {
        ...form,
        business_type: parseInt(form.business_type, 10),
      };
      return api.post('/projects/api/projects/', payload);
    },
    onSuccess: (response) => {
      const project = response.data;
      navigate(`/projects/${project.id}`);
    },
    onError: (err) => {
      const data = err.response?.data;
      let msg = 'خطا در ایجاد پروژه.';
      if (data) {
        if (typeof data === 'string') {
          msg = data;
        } else if (Array.isArray(data)) {
          msg = data.join('، ');
        } else if (typeof data === 'object') {
          msg = Object.entries(data)
            .map(([field, val]) => {
              const text = Array.isArray(val) ? val.join('، ') : val;
              return `${field}: ${text}`;
            })
            .join(' | ');
        }
      }
      setError(msg);
    },
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.title || !form.business_type || !form.description.trim()) {
      setError('عنوان، توضیحات و نوع کسب‌وکار الزامی است');
      return;
    }
    setError(null);
    mutation.mutate();
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '600px' }}>
      <h2 className="mb-4 text-center">ایجاد پروژه جدید</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">عنوان پروژه</label>
          <input type="text" className="form-control" name="title" value={form.title} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">توضیحات</label>
          <textarea className="form-control" rows="3" name="description" value={form.description} onChange={handleChange}></textarea>
        </div>
        <div className="mb-3">
          <label className="form-label">نوع کسب‌وکار</label>
          {loadingCats ? (
            <p>در حال دریافت...</p>
          ) : (
            <select className="form-select" name="business_type" value={form.business_type} onChange={handleChange} required>
              <option value="">انتخاب کنید...</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          )}
        </div>
        <button className="btn btn-primary w-100" type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? 'در حال ایجاد...' : 'ایجاد و ادامه'}
        </button>
      </form>
    </div>
  );
}

export default NewProjectPage; 