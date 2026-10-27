# LLM-Generated Tests for C# Libraries

این مخزن یک بررسی تجربی قابل‌تکرار از فاصله‌ی احتمالی بین code coverage و mutation score در تست‌های تولیدشده توسط LLM برای کد C# است. هدف، ادعای تازگی نیست؛ فقط بررسی می‌کنیم آیا این الگوی شناخته‌شده در چند کتابخانه‌ی کوچک .NET هم دیده می‌شود.

## وضعیت فعلی

این پروژه مرحله‌به‌مرحله اجرا می‌شود. `libs.csv` نامزدها را نگه می‌دارد و فقط کتابخانه‌هایی که واقعاً clone، build و test شوند وارد تحلیل می‌شوند. هیچ نتیجه‌ای تا قبل از اجرای واقعی ابزارها وارد CSV نتایج نمی‌شود.

## روش

- هشت کتابخانه‌ی pure-logic با commit ثابت بررسی می‌شوند.
- برای هر کتابخانه ۳ تا ۵ فایل source انتخاب و در `libs.csv` ثبت می‌شود.
- یک مدل از `LLM_MODEL`، دمای ثابت `0.2` و کلید فقط از `LLM_API_KEY` استفاده می‌کند.
- برای هر کلاس، سه تکرار از prompt پایه و سه تکرار از prompt بازخوردی اجرا می‌شود.
- خطای compile، تست ناموفق، timeout و حذف تست‌های ناموفق روی کد اصلی ثبت می‌شوند و پنهان نمی‌مانند.
- coverage با Coverlet و mutation score با Stryker.NET، محدود به فایل‌های انتخاب‌شده، اندازه‌گیری می‌شود.

## اجرا

هر مرحله یک فرمان جدا دارد:

```powershell
python src/select_libs.py
python src/generate.py --library Ardalis.GuardClauses --strategy basic --repeat 1 --class-file src/GuardClauses/Guard.cs
python src/validate.py --library Ardalis.GuardClauses
python src/measure.py --library Ardalis.GuardClauses --suite human
python src/feedback_round.py --library Ardalis.GuardClauses
python src/analyze.py
python src/survivors.py
```

تنظیمات مدل:

```powershell
$env:LLM_API_KEY = "..."
$env:LLM_MODEL = "..."
$env:LLM_BASE_URL = "https://api.openai.com/v1"
```

کلید API در فایل، prompt، CSV یا git ذخیره نمی‌شود.

## محدودیت‌ها

تهدیدهای اعتبار شامل احتمال آلودگی داده‌ی آموزشی به‌دلیل عمومی بودن کتابخانه‌ها، استفاده از یک مدل، تعداد کم کتابخانه‌ها، محدود بودن mutation operatorها به Stryker.NET و برچسب‌گذاری دستی توسط یک نفر است. خطای build یا timeout باعث حذف خاموش داده نمی‌شود.

## ساختار

- `src/`: مراحل pipeline
- `data/raw/`: خروجی خام مدل و گزارش ابزارها
- `data/results/`: CSVهای قابل تحلیل
- `analysis/`: نمودارها و خلاصه‌های آماری
- `report/`: اسکلت گزارش ۶ تا ۸ صفحه‌ای
