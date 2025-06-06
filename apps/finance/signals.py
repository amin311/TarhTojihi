from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProjectFinancialData
from .services import npv, irr, payback_period


@receiver(post_save, sender=ProjectFinancialData)
def calculate_financial_metrics(sender, instance: ProjectFinancialData, **kwargs):
    """پس از ذخیره داده‌های مالی، شاخص‌ها را محاسبه و ذخیره می‌کند."""
    try:
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
        total = 0
        if isinstance(instance.data, list):
            for row in instance.data:
                for value in row.values():
                    try:
                        total += float(value)
                    except (TypeError, ValueError):
                        pass
        metrics['total'] = total

        if metrics:
            instance.computed_metrics = metrics
            # از update_fields استفاده نکنید چون ممکن است سیگنال مجدد صدا زده شود
            ProjectFinancialData.objects.filter(pk=instance.pk).update(computed_metrics=metrics)
    except Exception as exc:
        # در صورت خطا، از ایجاد حلقه بی‌نهایت جلوگیری می‌شود و خطا لاگ می‌شود
        print(f"[Finance] Metric calculation failed: {exc}") 