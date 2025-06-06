import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '@/api/axios';
import FinancialWizard from '@/components/FinancialWizard';
import FinanceBoard from '@/components/FinanceBoard';

function ProjectDetailPage() {
  const { id } = useParams();
  const [isGenerating, setIsGenerating] = useState(false);

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: async () => {
      const { data } = await api.get(`/projects/api/projects/${id}/`);
      return data;
    },
  });

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    try {
      const response = await api.get(`/projects/api/projects/${id}/generate-report/`, {
        responseType: 'blob', // مهم: برای دریافت فایل
      });
      
      // ساخت لینک دانلود در مرورگر
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `TarhTojihi_Project_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

    } catch (error) {
      console.error("Error generating report:", error);
      alert('خطا در تولید گزارش. لطفاً پیش‌نیازهای سرور را بررسی کنید.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (isLoading) return <p>در حال بارگذاری...</p>;
  if (!project) return <p>پروژه یافت نشد.</p>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>{project.title}</h2>
        <button className="btn btn-success" onClick={handleGenerateReport} disabled={isGenerating}>
          {isGenerating ? 'در حال ساخت گزارش...' : 'دانلود گزارش PDF'}
        </button>
      </div>
      <p>{project.description}</p>

      <h4 className="mt-5 mb-3">ورود داده‌های مالی</h4>
      <FinanceBoard projectId={id} categoryId={project.business_type} />
    </div>
  );
}

export default ProjectDetailPage; 