import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/api/axios';
import DynamicTable from './DynamicTable';

function FinancialWizard({ projectId, categoryId }) {
  const queryClient = useQueryClient();
  const [currentTableIdx, setCurrentTableIdx] = useState(0);

  // دریافت جدول‌های مالی تعریف‌شده از ادمین
  const { data: tables = [], isLoading: loadingTables } = useQuery({
    queryKey: ['financialTables', categoryId],
    enabled: !!categoryId,
    queryFn: async () => {
      const { data } = await api.get('/categories/api/financial-tables/', {
        params: { category: categoryId },
      });
      return data;
    },
  });

  const currentTable = tables[currentTableIdx];

  // داده‌های موجود برای این جدول و پروژه
  const { data: existingData, isLoading: loadingExisting } = useQuery({
    queryKey: ['projectFinData', projectId, currentTable?.id],
    enabled: !!currentTable,
    queryFn: async () => {
      const { data } = await api.get('/finance/api/project-financial-data/', {
        params: { project: projectId, financial_table: currentTable.id },
      });
      let list = data;
      if (Array.isArray(data)) {
        list = data;
      } else if (data && data.results) {
        list = data.results;
      }
      return list && list.length ? list[0] : null;
    },
  });

  // ذخیره داده‌های یک جدول (Hook باید قبل از Conditional Return باشد)
  const mutation = useMutation({
    mutationFn: async ({ tableId, payload, id }) => {
      if (id) {
        return api.patch(`/finance/api/project-financial-data/${id}/`, {
          data: payload,
        });
      }
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

  if (!currentTable) return <p>تمام گام‌ها تکمیل شد.</p>;

  if (loadingExisting) return <p>در حال بارگذاری داده‌های جدول...</p>;

  const handleSubmit = (rows) => {
    if (existingData) {
      mutation.mutate({ tableId: currentTable.id, payload: rows, id: existingData.id });
    } else {
      mutation.mutate({ tableId: currentTable.id, payload: rows });
    }
  };

  const initialRows = existingData ? existingData.data : [{}];

  return (
    <div className="mb-5">
      <h5>{currentTable.name}</h5>
      <DynamicTable
        fields={currentTable.fields}
        onSubmit={handleSubmit}
        submitting={mutation.isPending}
        initialRows={initialRows}
      />
      <p className="text-muted mt-2">
        {currentTableIdx + 1} / {tables.length}
      </p>
    </div>
  );
}

export default FinancialWizard; 