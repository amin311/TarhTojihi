import React, { useState, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/api/axios';
import DynamicTable from './DynamicTable';

function TextTable({ initialText, onSave, loading }) {
  const [value, setValue] = React.useState(initialText || '');
  return (
    <div>
      <textarea
        className="form-control"
        style={{ minHeight: '200px' }}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <button disabled={loading} className="btn btn-primary mt-2" onClick={() => onSave(value)}>
        ذخیره
      </button>
    </div>
  );
}

function AutoSummary({ metrics }) {
  if (!metrics) return <p>داده‌ای محاسبه نشده است.</p>;
  return (
    <div className="alert alert-secondary">
      {Object.entries(metrics).map(([k, v]) => (
        <p key={k} className="mb-1">
          <strong>{k}:</strong> {v}
        </p>
      ))}
    </div>
  );
}

// ترتیب دلخواه فصل‌ها
const SECTION_ORDER = ['capex', 'opex', 'revenue', 'analysis'];
const SECTION_LABELS = {
  capex: 'سرمایه‌گذاری ثابت',
  opex: 'هزینه‌های متغیر',
  revenue: 'درآمد / فروش',
  analysis: 'تحلیل و شاخص‌ها',
};

function FinanceBoard({ projectId, categoryId }) {
  const queryClient = useQueryClient();
  const [activeSection, setActiveSection] = useState('capex');
  const [activeTabIdx, setActiveTabIdx] = useState(0);

  // دریافت تمام جداول آن دسته‌بندی
  const { data: tables = [], isLoading } = useQuery({
    queryKey: ['financialTablesAll', categoryId],
    enabled: !!categoryId,
    queryFn: async () => {
      const { data } = await api.get('/categories/api/financial-tables/', {
        params: { category: categoryId },
      });
      return data;
    },
  });

  const grouped = useMemo(() => {
    const g = {};
    tables.forEach((t) => {
      if (!g[t.section]) g[t.section] = [];
      g[t.section].push(t);
    });
    // مرتب‌سازی در هر گروه
    Object.keys(g).forEach((k) => {
      g[k].sort((a, b) => a.id - b.id);
    });
    return g;
  }, [tables]);

  // در صورتی که تب فعلی بعد از ریفِرِش وجود نداشته باشد ریست کنیم
  const currentSectionTables = grouped[activeSection] || [];
  const currentTable = currentSectionTables[activeTabIdx];

  // داده‌های موجود جدول
  const { data: existingData } = useQuery({
    queryKey: ['projectFinData', projectId, currentTable?.id],
    enabled: !!currentTable,
    queryFn: async () => {
      const { data } = await api.get('/finance/api/project-financial-data/', {
        params: { project: projectId, financial_table: currentTable.id },
      });
      return Array.isArray(data) && data.length ? data[0] : null;
    },
  });

  // دریافت فرمول‌های جدول
  const { data: formulas = [] } = useQuery({
    queryKey: ['formulas', currentTable?.id],
    enabled: !!currentTable && currentTable.table_type === 'grid',
    queryFn: async () => {
      const { data } = await api.get('/finance/api/formulas/', {
        params: { financial_table: currentTable.id },
      });
      return data;
    },
  });

  // mutation برای ذخیره
  const mutation = useMutation({
    mutationFn: async ({ payload }) => {
      if (existingData) {
        return api.patch(`/finance/api/project-financial-data/${existingData.id}/`, { data: payload });
      }
      return api.post('/finance/api/project-financial-data/', {
        project: projectId,
        financial_table: currentTable.id,
        data: payload,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projectFinData', projectId, currentTable.id]);
      alert('ذخیره شد');
    },
  });

  if (isLoading) return <p>در حال دریافت جداول...</p>;
  if (!tables.length) return <p>برای این دسته‌بندی جدولی تعریف نشده است.</p>;

  const handleSubmit = (payload) => {
    mutation.mutate({ payload });
  };

  const renderContent = () => {
    if (!currentTable) return <p>جدولی در این فصل وجود ندارد.</p>;

    if (currentTable.table_type === 'grid') {
      const initialRows = Array.isArray(existingData?.data) && existingData.data.length ? existingData.data : [{}];
      return (
        <DynamicTable
          fields={currentTable.fields}
          onSubmit={handleSubmit}
          submitting={mutation.isPending}
          initialRows={initialRows}
          formulas={formulas}
        />
      );
    }

    if (currentTable.table_type === 'text') {
      const initialText = typeof existingData?.data === 'string' ? existingData.data : '';
      return <TextTable initialText={initialText} onSave={handleSubmit} loading={mutation.isPending} />;
    }

    if (currentTable.table_type === 'auto') {
      return <AutoSummary metrics={existingData?.computed_metrics} />;
    }

    return <p>نوع جدول ناشناخته است.</p>;
  };

  return (
    <div className="d-flex">
      {/* منوی عمودی فصل‌ها */}
      <ul className="list-group me-3" style={{ minWidth: '180px' }}>
        {SECTION_ORDER.map((sec) => (
          <li
            key={sec}
            className={`list-group-item list-group-item-action ${activeSection === sec ? 'active' : ''}`}
            role="button"
            onClick={() => {
              setActiveSection(sec);
              setActiveTabIdx(0);
            }}
          >
            {SECTION_LABELS[sec] || sec}
          </li>
        ))}
      </ul>

      <div className="flex-grow-1">
        {/* تب‌های افقی */}
        <ul className="nav nav-tabs mb-3">
          {currentSectionTables.map((tbl, idx) => (
            <li className="nav-item" key={tbl.id}>
              <button
                className={`nav-link ${idx === activeTabIdx ? 'active' : ''}`}
                onClick={() => setActiveTabIdx(idx)}
              >
                {tbl.name}
              </button>
            </li>
          ))}
        </ul>

        {renderContent()}
      </div>
    </div>
  );
}

export default FinanceBoard; 