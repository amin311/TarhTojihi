import { create, all } from 'mathjs';

const math = create(all);

export default function useFormulaEngine(rows, fields, formulas) {
  const metrics = {};
  if (!formulas?.length) return metrics;

  formulas.forEach((f) => {
    const scope = {};

    // جمع هر ستون عددی
    fields.forEach((fld) => {
      const colSum = rows.reduce((acc, r) => acc + (parseFloat(r[fld.name]) || 0), 0);
      scope[`sum_${fld.name}`] = colSum;
    });

    // هر کلید داخل ردیف اول را نیز به scope اضافه کنیم (در صورت درج مستقیم)
    if (rows[0]) {
      Object.keys(rows[0]).forEach((k) => {
        try {
          scope[k] = parseFloat(rows[0][k]) || rows[0][k];
        } catch {
          scope[k] = rows[0][k];
        }
      });
    }

    try {
      const val = math.evaluate(f.expression, scope);
      metrics[f.result_key] = val;
    } catch (err) {
      metrics[f.result_key] = 'خطا';
    }
  });

  return metrics;
} 