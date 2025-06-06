import numpy_financial as npf
from typing import List


def npv(rate: float, cashflows: List[float]) -> float:
    """محاسبه NPV بر اساس نرخ تنزیل و جریان‌های نقدی."""
    return float(npf.npv(rate, cashflows))


def irr(cashflows: List[float]) -> float:
    """محاسبه IRR (بازده داخلی) از جریان‌های نقدی."""
    return float(npf.irr(cashflows))


def payback_period(initial_investment: float, cashflows: List[float]) -> float:
    """محاسبه دوره بازگشت سرمایه به صورت تقریبی."""
    cumulative = -initial_investment
    for idx, cf in enumerate(cashflows, start=1):
        cumulative += cf
        if cumulative >= 0:
            return idx  # تعدادی دوره (مثلاً سال) تا بازگشت
    return -1  # بازگشتی اتفاق نیافتاده است 