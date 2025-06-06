import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
  withCredentials: false,
});

// add token from localStorage if exists
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// ریفرش توکن ساده و هدایت در خطاهای احراز هویت
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;

    // اگر 401 یا 403 و مسیر /auth/token/ نیست
    if ((status === 401 || status === 403) && !originalRequest._retry && !originalRequest.url.includes('/auth/token/')) {
      originalRequest._retry = true;

      const refresh = localStorage.getItem('refresh');
      if (refresh) {
        try {
          const { data } = await api.post('/auth/token/refresh/', { refresh });
          localStorage.setItem('token', data.access);
          api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
          originalRequest.headers['Authorization'] = `Bearer ${data.access}`;
          return api(originalRequest);
        } catch (e) {
          // refresh ناکام → حذف توکن و هدایت به Login
        }
      }

      // پاک‌سازی و هدایت
      localStorage.removeItem('token');
      localStorage.removeItem('refresh');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  },
);

export default api; 