import React, { useState } from 'react';

function DynamicTable({ fields, onSubmit, submitting }) {
  const [rows, setRows] = useState([{}]);

  const handleChange = (rowIdx, fieldName, value) => {
    setRows((prev) => {
      const updated = [...prev];
      updated[rowIdx] = { ...updated[rowIdx], [fieldName]: value };
      return updated;
    });
  };

  const addRow = () => setRows((prev) => [...prev, {}]);
  const removeRow = (idx) => setRows((prev) => prev.filter((_, i) => i !== idx));

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(rows);
  };

  return (
    <form onSubmit={handleSubmit}>
      <table className="table table-bordered">
        <thead>
          <tr>
            {fields.map((f) => (
              <th key={f.id}>{f.name}</th>
            ))}
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIdx) => (
            <tr key={rowIdx}>
              {fields.map((f) => (
                <td key={f.id}>
                  {f.field_type === 'numeric' ? (
                    <input
                      type="number"
                      className="form-control"
                      value={row[f.name] || ''}
                      onChange={(e) => handleChange(rowIdx, f.name, e.target.value)}
                    />
                  ) : (
                    <input
                      type="text"
                      className="form-control"
                      value={row[f.name] || ''}
                      onChange={(e) => handleChange(rowIdx, f.name, e.target.value)}
                    />
                  )}
                </td>
              ))}
              <td>
                <button type="button" className="btn btn-sm btn-danger" onClick={() => removeRow(rowIdx)}>
                  حذف
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button type="button" className="btn btn-secondary me-2" onClick={addRow}>
        افزودن ردیف
      </button>
      <button type="submit" className="btn btn-primary" disabled={submitting}>
        {submitting ? 'در حال ذخیره...' : 'ذخیره و ادامه'}
      </button>
    </form>
  );
}

export default DynamicTable; 