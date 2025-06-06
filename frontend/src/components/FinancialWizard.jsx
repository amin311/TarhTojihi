import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/api/axios';
import DynamicTable from './DynamicTable';

function FinancialWizard({ projectId }) {
  const queryClient = useQueryClient();
  const [currentTableIdx, setCurrentTableIdx] = useState(0);

  // دریافت جدول‌های مالی تعریف‌شده از ادمین
  const { data: tables = [], isLoading: loadingTables } = useQuery({
    queryKey: ['financialTables'],
    queryFn: async () => {
      const { data } = await api.get('/categories/api/financial-tables/');
      return data;
    },
  });

  // ذخیره داده‌های یک جدول
  const mutation = useMutation({
    mutationFn: async ({ tableId, payload }) => {
      return api.post('/finance/api/project-financial-data/', {
        project: projectId,
        financial_table: tableId,
        data: payload,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projectFinData', projectId]);
      alert('داده‌ها ذخیره شد');
      setCurrentTableIdx((prev) => prev + 1);
    },
  });

  if (loadingTables) return <p>دریافت ساختار جداول...</p>;
  if (!tables.length) return <p>جدولی تعریف نشده است.</p>;

  const currentTable = tables[currentTableIdx];

  if (!currentTable) return <p>تمام گام‌ها تکمیل شد.</p>;

  const handleSubmit = (rows) => {
    mutation.mutate({ tableId: currentTable.id, payload: rows });
  };

  return (
    <div className="mb-5">
      <h5>{currentTable.name}</h5>
      <DynamicTable fields={currentTable.fields} onSubmit={handleSubmit} submitting={mutation.isPending} />
      <p className="text-muted mt-2">
        {currentTableIdx + 1} / {tables.length}
      </p>
    </div>
  );
}

export default FinancialWizard; 