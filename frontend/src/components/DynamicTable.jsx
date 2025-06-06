import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const DynamicTable = ({ tableId, projectId, onDataChange }) => {
  const [tableData, setTableData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editingCell, setEditingCell] = useState(null);
  const [formulaSuggestions, setFormulaSuggestions] = useState([]);
  const [showFormulaSuggestions, setShowFormulaSuggestions] = useState(false);

  // دریافت داده‌های جدول
  const fetchTableData = useCallback(async () => {
    try {
      const response = await axios.get(`/api/tables/${tableId}/data/`);
      setTableData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('خطا در دریافت داده‌های جدول:', error);
      setLoading(false);
    }
  }, [tableId]);

  // دریافت پیشنهادات فرمول
  const fetchFormulaSuggestions = useCallback(async () => {
    try {
      const response = await axios.get(`/api/formula-suggestions/?project_id=${projectId}`);
      setFormulaSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('خطا در دریافت پیشنهادات فرمول:', error);
    }
  }, [projectId]);

  useEffect(() => {
    fetchTableData();
    fetchFormulaSuggestions();
  }, [fetchTableData, fetchFormulaSuggestions]);

  // به‌روزرسانی بلادرنگ سلول
  const updateCell = async (rowId, columnId, value) => {
    try {
      const response = await axios.post('/api/realtime-update/', {
        project_id: projectId,
        table_id: tableId,
        row_id: rowId,
        column_id: columnId,
        value: value
      });

      if (response.data.success) {
        // به‌روزرسانی داده‌های محلی
        setTableData(prevData => {
          const newData = { ...prevData };
          
          // به‌روزرسانی سلول فعلی
          const targetRow = newData.rows.find(row => row.id === rowId);
          if (targetRow) {
            const columnName = newData.columns.find(col => col.id === columnId)?.name;
            if (columnName && targetRow.cells[columnName]) {
              targetRow.cells[columnName].value = response.data.updated_value;
            }
          }

          // به‌روزرسانی سلول‌های وابسته
          response.data.dependent_changes.forEach(change => {
            if (change.table_id === tableId) {
              const depRow = newData.rows.find(row => row.id === change.row_id);
              if (depRow) {
                const depColumnName = newData.columns.find(col => col.id === change.column_id)?.name;
                if (depColumnName && depRow.cells[depColumnName]) {
                  depRow.cells[depColumnName].value = change.value;
                }
              }
            }
          });

          return newData;
        });

        // اطلاع‌رسانی به کامپوننت والد
        if (onDataChange) {
          onDataChange(response.data);
        }
      }
    } catch (error) {
      console.error('خطا در به‌روزرسانی سلول:', error);
      alert('خطا در به‌روزرسانی سلول: ' + error.message);
    }
  };

  // شروع ویرایش سلول
  const startEditing = (rowId, columnId, currentValue) => {
    setEditingCell({
      rowId,
      columnId,
      value: currentValue || ''
    });
  };

  // پایان ویرایش سلول
  const finishEditing = async () => {
    if (editingCell) {
      await updateCell(editingCell.rowId, editingCell.columnId, editingCell.value);
      setEditingCell(null);
    }
  };

  // لغو ویرایش
  const cancelEditing = () => {
    setEditingCell(null);
  };

  // تغییر مقدار در حین ویرایش
  const handleEditChange = (value) => {
    setEditingCell(prev => ({ ...prev, value }));
  };

  // اضافه کردن ستون جدید
  const addColumn = async () => {
    const name = prompt('نام ستون:');
    const type = prompt('نوع ستون (text/number/calculated/reference):', 'text');
    const unit = prompt('واحد (اختیاری):') || '';
    const formula = type === 'calculated' ? prompt('فرمول محاسباتی:') || '' : '';

    if (name) {
      try {
        const response = await axios.post(`/api/tables/${tableId}/add_column/`, {
          name,
          type,
          unit,
          formula,
          order: (tableData?.columns?.length || 0) + 1
        });

        if (response.data.id) {
          await fetchTableData(); // به‌روزرسانی داده‌ها
        }
      } catch (error) {
        console.error('خطا در اضافه کردن ستون:', error);
        alert('خطا در اضافه کردن ستون');
      }
    }
  };

  // اضافه کردن ردیف جدید
  const addRow = async () => {
    const label = prompt('برچسب ردیف:');
    
    if (label) {
      try {
        const response = await axios.post(`/api/tables/${tableId}/add_row/`, {
          label,
          order: (tableData?.rows?.length || 0) + 1
        });

        if (response.data.id) {
          await fetchTableData(); // به‌روزرسانی داده‌ها
        }
      } catch (error) {
        console.error('خطا در اضافه کردن ردیف:', error);
        alert('خطا در اضافه کردن ردیف');
      }
    }
  };

  // محاسبه مجدد جدول
  const recalculateTable = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`/api/tables/${tableId}/recalculate/`);
      
      if (response.data.success) {
        setTableData(response.data.data);
        alert('جدول با موفقیت محاسبه مجدد شد');
      }
    } catch (error) {
      console.error('خطا در محاسبه مجدد:', error);
      alert('خطا در محاسبه مجدد');
    } finally {
      setLoading(false);
    }
  };

  // رندر سلول
  const renderCell = (row, column) => {
    const cellData = row.cells[column.name];
    const isEditing = editingCell && editingCell.rowId === row.id && editingCell.columnId === column.id;
    
    if (isEditing) {
      return (
        <div className="edit-cell">
          <input
            type="text"
            value={editingCell.value}
            onChange={(e) => handleEditChange(e.target.value)}
            onBlur={finishEditing}
            onKeyDown={(e) => {
              if (e.key === 'Enter') finishEditing();
              if (e.key === 'Escape') cancelEditing();
            }}
            autoFocus
            className="cell-input"
          />
          {column.type === 'calculated' && (
            <div className="formula-help">
              <small>فرمول: {column.formula}</small>
            </div>
          )}
        </div>
      );
    }

    const displayValue = cellData?.value || '';
    const cellClass = `table-cell ${column.type === 'calculated' ? 'calculated' : ''} ${column.type === 'reference' ? 'reference' : ''}`;

    return (
      <div
        className={cellClass}
        onClick={() => startEditing(row.id, column.id, displayValue)}
        title={column.type === 'calculated' ? `فرمول: ${column.formula}` : ''}
      >
        {displayValue}
        {cellData?.unit && <span className="unit"> {cellData.unit}</span>}
      </div>
    );
  };

  if (loading) {
    return <div className="loading">در حال بارگذاری...</div>;
  }

  if (!tableData) {
    return <div className="error">خطا در بارگذاری جدول</div>;
  }

  return (
    <div className="dynamic-table-container">
      <div className="table-header">
        <h3>{tableData.name}</h3>
        <div className="table-actions">
          <button onClick={addColumn} className="btn btn-primary">
            افزودن ستون
          </button>
          <button onClick={addRow} className="btn btn-primary">
            افزودن ردیف
          </button>
          <button onClick={recalculateTable} className="btn btn-secondary">
            محاسبه مجدد
          </button>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="dynamic-table">
          <thead>
            <tr>
              <th>ردیف</th>
              {tableData.columns.map(column => (
                <th key={column.id} className={`column-${column.type}`}>
                  {column.name}
                  {column.unit && <span className="unit-header"> ({column.unit})</span>}
                  {column.type === 'calculated' && <span className="formula-indicator">📊</span>}
                  {column.type === 'reference' && <span className="reference-indicator">🔗</span>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.rows.map(row => (
              <tr key={row.id}>
                <td className="row-label">{row.label}</td>
                {tableData.columns.map(column => (
                  <td key={`${row.id}-${column.id}`}>
                    {renderCell(row, column)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* راهنمای فرمول‌ها */}
      {showFormulaSuggestions && (
        <div className="formula-suggestions">
          <h4>راهنمای فرمول‌ها</h4>
          <div className="suggestions-list">
            {formulaSuggestions.map((suggestion, index) => (
              <div key={index} className="suggestion-item">
                <code>{suggestion.syntax}</code>
                <span className="suggestion-desc">{suggestion.description}</span>
              </div>
            ))}
          </div>
          <button 
            onClick={() => setShowFormulaSuggestions(false)} 
            className="close-suggestions"
          >
            بستن
          </button>
        </div>
      )}

      <div className="table-footer">
        <button 
          onClick={() => setShowFormulaSuggestions(true)} 
          className="btn btn-link"
        >
          راهنمای فرمول‌ها
        </button>
        <small>
          آخرین به‌روزرسانی: {new Date().toLocaleString('fa-IR')}
        </small>
      </div>
    </div>
  );
};

export default DynamicTable; 