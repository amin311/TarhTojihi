# راهنمای فرمول‌های محاسباتی

## 🔢 انواع فرمول‌ها و محل استفاده

### ۱. فرمول‌های داخل ردیف
```python
# استفاده در: TableColumn.formula
'[this.متراژ] * [this.قیمت واحد]'

# مثال عملی در کد:
table_manager.add_column(
    table=land_table,
    name='جمع کل',
    column_type='calculated',
    order=4,
    unit='ریال',
    formula='[this.متراژ] * [this.قیمت واحد]'
)
```

### ۲. فرمول‌های مجموع ستون
```python
# استفاده در: TableColumn.formula
'SUM[ماشین‌آلات.جمع کل]'

# مثال عملی:
table_manager.add_column(
    summary_table,
    'مجموع ماشین‌آلات',
    'reference',
    2,
    'ریال',
    'SUM[ماشین‌آلات.جمع کل]'
)
```

### ۳. فرمول‌های ارجاع بین فصول
```python
# استفاده در: TableColumn.formula
'[سرمایه‌گذاری ثابت.خلاصه.مبلغ]'

# مثال عملی:
table_manager.add_column(
    final_table,
    'سرمایه ثابت',
    'reference',
    2,
    'ریال',
    '[سرمایه‌گذاری ثابت.خلاصه سرمایه‌گذاری.مبلغ]'
)
```

## 💾 کش محاسبات

### استفاده در Backend (services.py)
```python
# در کلاس CalculationEngine
def expensive_calculation(self):
    # بررسی کش
    cached = self.get_cached_calculation("total_project_cost")
    if cached:
        return cached
    
    # محاسبه مقدار جدید
    result = self._calculate_total_cost()
    
    # ذخیره در کش
    self.set_cached_calculation("total_project_cost", result)
    return result

# مثال در views.py
@action(detail=True, methods=['get'])
def project_summary(self, request, pk=None):
    project = self.get_object()
    calc_engine = CalculationEngine(project)
    
    # استفاده از کش برای بهینه‌سازی
    total_cost = calc_engine.get_cached_calculation("total_cost")
    if not total_cost:
        calc_engine.recalculate_project()
        total_cost = calc_engine.get_cached_calculation("total_cost")
    
    return Response({'total_cost': total_cost})
```

## ⚡ به‌روزرسانی بلادرنگ

### استفاده در Frontend (DynamicTable.jsx)
```javascript
// تابع به‌روزرسانی سلول
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
            // به‌روزرسانی سلول فعلی
            updateCurrentCell(response.data.updated_value);
            
            // به‌روزرسانی سلول‌های وابسته
            response.data.dependent_changes.forEach(change => {
                updateDependentCell(change);
            });
        }
    } catch (error) {
        console.error('خطا در به‌روزرسانی:', error);
    }
};

// استفاده در رویداد
<input 
    onBlur={() => updateCell(row.id, column.id, inputValue)}
    onKeyDown={(e) => {
        if (e.key === 'Enter') {
            updateCell(row.id, column.id, inputValue);
        }
    }}
/>
```

### مدیریت تغییرات وابسته
```javascript
// در کامپوننت DynamicTable
const handleDependentChanges = (changes) => {
    setTableData(prevData => {
        const newData = { ...prevData };
        
        changes.forEach(change => {
            const { table_id, row_id, column_id, value } = change;
            
            // اگر تغییر در همین جدول باشد
            if (table_id === tableId) {
                const targetRow = newData.rows.find(r => r.id === row_id);
                const targetColumn = newData.columns.find(c => c.id === column_id);
                
                if (targetRow && targetColumn) {
                    targetRow.cells[targetColumn.name].value = value;
                }
            }
        });
        
        return newData;
    });
    
    // اطلاع‌رسانی به جداول دیگر
    if (onDataChange) {
        onDataChange(changes);
    }
};
```

## 🔄 جریان کامل به‌روزرسانی

### ۱. کاربر تغییر می‌دهد
```javascript
// در frontend
await updateCell(rowId, columnId, newValue);
```

### ۲. Backend پردازش می‌کند
```python
# در views.py -> realtime_update
def realtime_update(request):
    # دریافت داده‌ها
    data = json.loads(request.body)
    
    # به‌روزرسانی سلول
    table_manager.update_cell_value(row, column, value)
    
    # پیدا کردن تغییرات وابسته
    dependent_changes = find_dependent_changes(...)
    
    return JsonResponse({
        'success': True,
        'updated_value': final_value,
        'dependent_changes': dependent_changes
    })
```

### ۳. Frontend به‌روزرسانی می‌کند
```javascript
// تمام سلول‌های وابسته خودکار به‌روزرسانی می‌شوند
response.data.dependent_changes.forEach(change => {
    updateCellDisplay(change);
});
```

## 📍 مکان‌های کاربرد در کد

### Backend:
- `apps/projects/models.py` → ذخیره فرمول‌ها در `TableColumn.formula`
- `apps/projects/services.py` → پردازش فرمول‌ها در `CalculationEngine`
- `apps/projects/views.py` → API برای به‌روزرسانی بلادرنگ
- `examples/create_sample_project.py` → مثال‌های عملی

### Frontend:
- `frontend/src/components/DynamicTable.jsx` → رابط کاربری و به‌روزرسانی فوری
- API calls برای ارتباط با backend

### کش:
- `apps/projects/models.py` → مدل `CalculationCache`
- `apps/projects/services.py` → متدهای `get_cached_calculation` و `set_cached_calculation`

## 🎯 مثال کامل

```python
# ۱. ایجاد جدول با فرمول
table = table_manager.create_table(chapter, 'محاسبات', 1)

# ۲. افزودن ستون‌های ورودی
table_manager.add_column(table, 'تعداد', 'number', 1, 'عدد')
table_manager.add_column(table, 'قیمت', 'number', 2, 'ریال')

# ۳. افزودن ستون محاسباتی
table_manager.add_column(
    table, 
    'جمع', 
    'calculated', 
    3, 
    'ریال',
    '[this.تعداد] * [this.قیمت]'  # <-- فرمول
)

# ۴. افزودن داده
row = table_manager.add_row(table, 'آیتم ۱', 1)
table_manager.update_cell_value(row, table.columns.get(name='تعداد'), '10')
table_manager.update_cell_value(row, table.columns.get(name='قیمت'), '1000')

# ۵. فرمول خودکار محاسبه می‌شود: 10 * 1000 = 10000
```

این سیستم امکان محاسبات پیشرفته و بلادرنگ را فراهم می‌کند! 🚀 