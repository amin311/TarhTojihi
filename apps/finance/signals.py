from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProjectFinancialData
from .services import npv, irr, payback_period
from django.db import models
from apps.categories.models import FinancialTable
from apps.finance.utils.formula_engine import safe_eval
from .models import FinancialFormula


@receiver(post_save, sender=ProjectFinancialData)
def calculate_financial_metrics(sender, instance: ProjectFinancialData, **kwargs):
    """پس از ذخیره داده‌های مالی، شاخص‌ها را محاسبه و ذخیره می‌کند."""
    try:
        # اگر جدول از نوع خودکار است، از محاسبه خودداری کنید تا از حلقه بی‌نهایت جلوگیری شود
        if instance.financial_table.table_type == 'auto':
            return

        # فرض: instance.data شامل کلیدی به‌نام 'cashflows' یک لیست است
        cashflows = instance.data.get('cashflows', []) if isinstance(instance.data, dict) else []
        rate = float(instance.data.get('discount_rate', 0.15)) if isinstance(instance.data, dict) else 0.15
        initial_investment = float(instance.data.get('initial_investment', 0)) if isinstance(instance.data, dict) else 0

        metrics = {}
        if cashflows:
            metrics['npv'] = npv(rate, cashflows)
            metrics['irr'] = irr(cashflows)
            metrics['payback_period'] = payback_period(initial_investment, cashflows)

        # مثال: جمع مقادیر عددی در داده‌ها (در صورت وجود)
        subtotal = 0
        if isinstance(instance.data, list):
            for row in instance.data:
                for value in row.values():
                    try:
                        subtotal += float(value)
                    except (TypeError, ValueError):
                        pass
        metrics['subtotal'] = subtotal

        # ---- اجرای فرمول‌های سطح جدول ----
        formulas = FinancialFormula.objects.filter(financial_table=instance.financial_table, level='table')
        variables = {}
        # متغیرها: فیلدهای داده و متریک‌های موجود
        if isinstance(instance.data, dict):
            variables.update(instance.data)
        elif isinstance(instance.data, list):
            # جمع هر ستون عددی به عنوان متغیر sum_<fieldName>
            if instance.data:
                cols = instance.data[0].keys()
                for col in cols:
                    try:
                        variables[f'sum_{col}'] = sum(float(row.get(col, 0) or 0) for row in instance.data)
                    except Exception:
                        pass
        variables.update(metrics)

        for formula in formulas:
            try:
                metrics[formula.result_key] = safe_eval(formula.expression, variables)
            except Exception as exc:
                print(f'[Formula] اجرای فرمول {formula.result_key} خطا: {exc}')

        if metrics:
            instance.computed_metrics = metrics
            # از update_fields استفاده نکنید چون ممکن است سیگنال مجدد صدا زده شود
            ProjectFinancialData.objects.filter(pk=instance.pk).update(computed_metrics=metrics)

            # پس از به‌روزرسانی جدول، جمع هر فصل را نیز به‌روز کنیم (و فرمول‌های سطح فصل اجرا شوند)
            _update_section_totals(instance.project)
    except Exception as exc:
        # در صورت خطا، از ایجاد حلقه بی‌نهایت جلوگیری می‌شود و خطا لاگ می‌شود
        print(f"[Finance] Metric calculation failed: {exc}")


# helper

def _update_section_totals(project):
    sections = ['capex', 'opex', 'revenue', 'analysis']
    for sec in sections:
        auto_tbl, _ = FinancialTable.objects.get_or_create(
            category=project.business_type,
            name=f'جمع {sec.upper()}',
            defaults={'section': sec, 'table_type': 'auto'},
        )
        subtotal = ProjectFinancialData.objects.filter(
            project=project,
            financial_table__section=sec,
            financial_table__table_type='grid',
        ).aggregate(models.Sum('computed_metrics__subtotal'))['computed_metrics__subtotal__sum'] or 0
        ProjectFinancialData.objects.update_or_create(
            project=project,
            financial_table=auto_tbl,
            defaults={'data': {}, 'computed_metrics': {'subtotal': subtotal}},
        )

        # فرمول‌های سطح فصل
        formulas = FinancialFormula.objects.filter(financial_table=None, level='section') | FinancialFormula.objects.filter(financial_table=auto_tbl, level='section')
        metrics = {'subtotal': subtotal}
        variables = {'subtotal': subtotal}
        for formula in formulas:
            try:
                metrics[formula.result_key] = safe_eval(formula.expression, variables)
            except Exception as exc:
                print(f'[Formula] خطا در فرمول فصل {formula.result_key}: {exc}')
        ProjectFinancialData.objects.filter(project=project, financial_table=auto_tbl).update(computed_metrics=metrics)

    # بعد از اتمام حلقه فصول، فرمول‌های سطح پروژه را محاسبه کنیم
    _evaluate_project_formulas(project)


def _evaluate_project_formulas(project):
    """محاسبه فرمول‌های کل پروژه (level='project') و ذخیره در جدول خودکار."""
    formulas = FinancialFormula.objects.filter(level='project')
    if not formulas.exists():
        return

    variables = {}
    pf_qs = ProjectFinancialData.objects.filter(project=project).exclude(computed_metrics=None)
    for pf in pf_qs:
        for key, val in (pf.computed_metrics or {}).items():
            variables[f"tbl_{pf.financial_table.id}__{key}"] = val

    results = {}
    for formula in formulas:
        try:
            results[formula.result_key] = safe_eval(formula.expression, variables)
        except Exception as exc:
            print(f'[Formula] خطا در فرمول پروژه {formula.result_key}: {exc}')

    if results:
        proj_tbl, _ = FinancialTable.objects.get_or_create(
            category=project.business_type,
            name='نتایج کل پروژه',
            defaults={'section': 'analysis', 'table_type': 'auto'},
        )
        ProjectFinancialData.objects.update_or_create(
            project=project,
            financial_table=proj_tbl,
            defaults={'data': {}, 'computed_metrics': results},
        ) 