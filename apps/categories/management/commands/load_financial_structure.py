from django.core.management.base import BaseCommand
from apps.categories.models import Category, Unit, FinancialTable, FinancialField


class Command(BaseCommand):
    """ایجاد واحدها، دسته‌بندی و ساختار جداول مالی متداول برای طرح توجیهی."""

    help = "Load default financial table structures (CAPEX, OPEX, etc.) for feasibility studies."

    def handle(self, *args, **options):
        # 1) واحدها
        unit_defs = [
            ("عدد", ""),
            ("مترمربع", "m²"),
            ("تن", "t"),
            ("کیلوگرم", "kg"),
            ("گیگاوات‌ساعت", "GWh"),
            ("Nm³", "Nm³"),
            ("میلیون تومان", "MIRR"),
            ("لیتر", "L"),
            ("کیلووات‌ساعت", "kWh"),
            ("درصد", "%"),
        ]
        units = {}
        for name, symbol in unit_defs:
            unit, _ = Unit.objects.get_or_create(name=name, defaults={"symbol": symbol})
            units[name] = unit

        # 2) دسته‌بندی‌ها و جدول‌هایشان
        categories_specs = {
            "صنایع تولیدی": {
                "description": "انواع طرح‌های تولید صنعتی",
                "tables": {
                    "زمین و آماده‌سازی سایت": [
                        ("شرح", "text", None),
                        ("مقدار", "numeric", units["مترمربع"]),
                        ("واحد", "text", None),
                        ("نرخ‌واحد", "numeric", units["میلیون تومان"]),
                        ("جمع‌کل", "numeric", units["میلیون تومان"]),
                    ],
                    "ساختمان و سازه‌ها": [
                        ("شرح", "text", None),
                        ("زیربنا", "numeric", units["مترمربع"]),
                        ("نرخ‌هر مترمربع", "numeric", units["میلیون تومان"]),
                        ("جمع‌کل", "numeric", units["میلیون تومان"]),
                    ],
                    "ماشین‌آلات تولیدی": [
                        ("شرح", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("نرخ‌واحد", "numeric", units["میلیون تومان"]),
                        ("مجموع", "numeric", units["میلیون تومان"]),
                    ],
                    "تأسیسات فنی": [
                        ("شرح", "text", None),
                        ("ظرفیت", "text", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "مواد اولیه و بسته‌بندی": [
                        ("شرح", "text", None),
                        ("مقدارسالیانه", "numeric", units["تن"]),
                        ("نرخ‌واحد", "numeric", units["میلیون تومان"]),
                        ("جمع‌کل", "numeric", units["میلیون تومان"]),
                    ],
                    "دستمزد مستقیم": [
                        ("گروه شغلی", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("حقوق‌ماهانه", "numeric", units["میلیون تومان"]),
                        ("حقوق‌سالانه", "numeric", units["میلیون تومان"]),
                        ("مزایا", "numeric", units["میلیون تومان"]),
                        ("جمع کل", "numeric", units["میلیون تومان"]),
                    ],
                    "انرژی و سوخت": [
                        ("نوع انرژی", "text", None),
                        ("مصرف سالانه", "numeric", None),
                        ("واحد", "text", None),
                        ("نرخ واحد", "numeric", units["میلیون تومان"]),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "تعمیر و نگهداری جاری": [
                        ("شرح", "text", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "سربار تولید متغیر": [
                        ("شرح", "text", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "هزینه‌های توزیع و فروش": [
                        ("شرح", "text", None),
                        ("پایه", "numeric", units["میلیون تومان"]),
                        ("درصد", "numeric", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "صورت سود و زیان": [
                        ("سرفصل", "text", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "نقطه سر به سر": [
                        ("شاخص", "text", None),
                        ("مقدار", "numeric", None),
                        ("واحد", "text", None),
                    ],
                },
            },
            "خدماتی": {
                "description": "پروژه‌های خدماتی و IT",
                "tables": {
                    "دفتر و مبلمان": [
                        ("شرح", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("نرخ‌واحد", "numeric", units["میلیون تومان"]),
                        ("جمع‌کل", "numeric", units["میلیون تومان"]),
                    ],
                    "تجهیزات IT": [
                        ("شرح", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "حقوق و دستمزد": [
                        ("سمت", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("حقوق ماهانه", "numeric", units["میلیون تومان"]),
                        ("حقوق سالانه", "numeric", units["میلیون تومان"]),
                    ],
                    "هزینه‌های عملیاتی": [
                        ("شرح", "text", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                },
            },
            "کشاورزی": {
                "description": "طرح‌های کشاورزی و دامپروری",
                "tables": {
                    "زمین و آماده‌سازی خاک": [
                        ("شرح", "text", None),
                        ("مساحت", "numeric", units["مترمربع"]),
                        ("هزینه", "numeric", units["میلیون تومان"]),
                    ],
                    "سازه و تجهیزات مزرعه": [
                        ("شرح", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                    "نهال/دام اولیه": [
                        ("شرح", "text", None),
                        ("تعداد", "numeric", units["عدد"]),
                        ("قیمت واحد", "numeric", units["میلیون تومان"]),
                        ("جمع", "numeric", units["میلیون تومان"]),
                    ],
                    "مواد مصرفی سالانه": [
                        ("شرح", "text", None),
                        ("مقدار", "numeric", None),
                        ("مبلغ", "numeric", units["میلیون تومان"]),
                    ],
                },
            },
        }

        # جداول مرسوم هزینه‌های متغیر (OPEX) برای همه دسته‌ها
        opex_common_tables = {
            "مواد اولیه": [
                ("عنوان", "text", None),
                ("مقدار مصرف سالانه", "numeric", units.get("تن")),
                ("نرخ واحد", "numeric", units["میلیون تومان"]),
                ("جمع", "numeric", units["میلیون تومان"]),
            ],
            "حقوق و دستمزد غیرمستقیم": [
                ("سمت", "text", None),
                ("تعداد", "numeric", units["عدد"]),
                ("حقوق ماهانه", "numeric", units["میلیون تومان"]),
                ("حقوق سالانه", "numeric", units["میلیون تومان"]),
            ],
            "هزینه انرژی و سوخت": [
                ("نوع انرژی", "text", None),
                ("مصرف سالانه", "numeric", None),
                ("واحد", "text", None),
                ("نرخ واحد", "numeric", units["میلیون تومان"]),
                ("مبلغ", "numeric", units["میلیون تومان"]),
            ],
            "نگهداری و تعمیرات": [
                ("شرح", "text", None),
                ("مبلغ", "numeric", units["میلیون تومان"]),
            ],
            "هزینه عمومی و اداری": [
                ("شرح", "text", None),
                ("مبلغ", "numeric", units["میلیون تومان"]),
            ],
            "بازاریابی و فروش": [
                ("شرح", "text", None),
                ("درصد از فروش", "numeric", units["درصد"]),
                ("مبلغ", "numeric", units["میلیون تومان"]),
            ],
        }

        # جداول مرسوم درآمد/فروش
        revenue_common_tables = {
            "فروش محصولات/خدمات": [
                ("محصول/خدمت", "text", None),
                ("ظرفیت تولید/ارائه", "numeric", None),
                ("واحد", "text", None),
                ("نرخ فروش", "numeric", units["میلیون تومان"]),
                ("درآمد سالانه", "numeric", units["میلیون تومان"]),
            ],
            "سایر درآمدها": [
                ("شرح", "text", None),
                ("مبلغ", "numeric", units["میلیون تومان"]),
            ],
        }

        # جداول را ایجاد کنیم (برای هر دسته‌بندی)
        for cat_name, cat_data in categories_specs.items():
            cat_obj, _ = Category.objects.get_or_create(name=cat_name, defaults={"description": cat_data.get("description", "")})
            for tbl_name, fields in cat_data["tables"].items():
                tbl, _ = FinancialTable.objects.get_or_create(category=cat_obj, name=tbl_name, defaults={"section": 'capex', "table_type": 'grid'})
                for idx, (name, ftype, unit) in enumerate(fields):
                    FinancialField.objects.get_or_create(
                        financial_table=tbl,
                        name=name,
                        defaults={"field_type": ftype, "unit": unit, "order": idx},
                    )

            # اضافه کردن جداول OPEX مشترک
            for tbl_name, fields in opex_common_tables.items():
                tbl, _ = FinancialTable.objects.get_or_create(category=cat_obj, name=tbl_name, defaults={"section": 'opex', "table_type": 'grid'})
                for idx, (name, ftype, unit) in enumerate(fields):
                    FinancialField.objects.get_or_create(
                        financial_table=tbl,
                        name=name,
                        defaults={"field_type": ftype, "unit": unit, "order": idx},
                    )

            # اضافه کردن جداول درآمد
            for tbl_name, fields in revenue_common_tables.items():
                tbl, _ = FinancialTable.objects.get_or_create(category=cat_obj, name=tbl_name, defaults={"section": 'revenue', "table_type": 'grid'})
                for idx, (name, ftype, unit) in enumerate(fields):
                    FinancialField.objects.get_or_create(
                        financial_table=tbl,
                        name=name,
                        defaults={"field_type": ftype, "unit": unit, "order": idx},
                    )

            # بخش‌های متنی عمومی
            for text_name in ["مقدمه", "تحلیل بازار", "مسائل فنی"]:
                FinancialTable.objects.get_or_create(
                    category=cat_obj,
                    name=text_name,
                    defaults={"section": 'analysis', "table_type": 'text'},
                )

            # جدول جمع فصول (auto)
            for sec in ['capex', 'opex', 'revenue', 'analysis']:
                FinancialTable.objects.get_or_create(
                    category=cat_obj,
                    name=f'جمع {sec.upper()}',
                    defaults={"section": sec, "table_type": 'auto'},
                )

        self.stdout.write(self.style.SUCCESS("ساختار جداول مالی همه دسته‌بندی‌ها ایجاد/به‌روزرسانی شد.")) 