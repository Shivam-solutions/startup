# Marg-ERP-Inspired Django Dashboard

**Important:** This project is *inspired by* common ERP dashboards and intentionally does **not** copy any proprietary design or branding from third-party products.

## What you get
- A complete Django project (Django 4.2) with a polished, professional dashboard UI.
- Sidebar navigation, top bar, stats cards, recent invoices table and quick-action buttons.
- Static files (CSS/JS/SVG) included.
- Ready to run locally with `runserver`.

## Quick start

1. Create virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate     # Windows (PowerShell)
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations and run server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. Open `http://127.0.0.1:8000/` in your browser.

## Notes
- This is a starter scaffold: menu links are placeholders that demonstrate layout and interactions.
- To extend: add models, forms, authentication, and the real features you need.

Enjoy!