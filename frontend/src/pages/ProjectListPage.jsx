import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '@/api/axios';

function ProjectListPage() {
  const { data: projects = [], isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const { data } = await api.get('/projects/api/projects/');
      return data;
    },
  });

  if (isLoading) return <p>در حال بارگذاری...</p>;

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>پروژه‌ها</h2>
        <Link to="/projects/new" className="btn btn-primary">پروژه جدید</Link>
      </div>
      <ul className="list-group">
        {projects.map((p) => (
          <li key={p.id} className="list-group-item d-flex justify-content-between align-items-center">
            {p.title}
            <Link to={`/projects/${p.id}`}>مشاهده</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProjectListPage; 