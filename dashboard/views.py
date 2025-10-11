from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from io import BytesIO
import difflib
import re

from .models import Stock


# ---------------- HOME PAGE ---------------- #
def home(request):
    menu = [
        {'name': 'Sales', 'icon': 'fa-shopping-cart'},
        {'name': 'Purchase', 'icon': 'fa-people-carry'},
        {'name': 'Inventory', 'icon': 'fa-archive'},
        {'name': 'Accounts', 'icon': 'fa-calculator'},
        {'name': 'Reports', 'icon': 'fa-chart-line'},
        {'name': 'Masters', 'icon': 'fa-database'},
        {'name': 'Billing', 'icon': 'fa-file-invoice-dollar'},
        {'name': 'POS', 'icon': 'fa-cash-register'},
        {'name': 'Settings', 'icon': 'fa-cog'},
    ]
    stats = [
        {'title':'Total Sales','value':'₹ 12,45,800'},
        {'title':'Pending Receipts','value':'₹ 2,48,000'},
        {'title':'Total Purchases','value':'₹ 5,88,200'},
        {'title':'GST Payable','value':'₹ 45,800'},
    ]
    quick_actions = ['New Sale', 'New Purchase', 'Add Item', 'New Customer', 'New Supplier', 'Receive Payment']
    recent = [
        {'invoice':'INV-1001','party':'ABC Traders','amount':'₹ 15,000','status':'Paid'},
        {'invoice':'INV-1002','party':'XYZ Enterprises','amount':'₹ 38,400','status':'Pending'},
        {'invoice':'INV-1003','party':'Home Needs','amount':'₹ 6,700','status':'Paid'},
    ]
    return render(request, 'dashboard/home.html', {
        'menu': menu,
        'stats': stats,
        'actions': quick_actions,
        'recent': recent
    })


# ---------------- SALES ENTRY PAGE ---------------- #
def sales_entry(request):
    menu = [
        {'name': 'Sales', 'icon': 'fa-shopping-cart'},
        {'name': 'Purchase', 'icon': 'fa-people-carry'},
        {'name': 'Inventory', 'icon': 'fa-archive'},
        {'name': 'Accounts', 'icon': 'fa-calculator'},
        {'name': 'Reports', 'icon': 'fa-chart-line'},
        {'name': 'Masters', 'icon': 'fa-database'},
        {'name': 'Billing', 'icon': 'fa-file-invoice-dollar'},
        {'name': 'POS', 'icon': 'fa-cash-register'},
        {'name': 'Settings', 'icon': 'fa-cog'},
    ]
    rows = range(20)
    return render(request, 'dashboard/sales_entry.html', {
        'menu': menu,
        'rows': rows
    })


# ---------------- INVENTORY PAGE ---------------- #
def inventory(request):
    from pandas import isna, to_datetime, read_excel, read_csv

    menu = [
        {'name': 'Sales', 'icon': 'fa-shopping-cart'},
        {'name': 'Purchase', 'icon': 'fa-people-carry'},
        {'name': 'Inventory', 'icon': 'fa-archive'},
        {'name': 'Accounts', 'icon': 'fa-calculator'},
        {'name': 'Reports', 'icon': 'fa-chart-line'},
        {'name': 'Masters', 'icon': 'fa-database'},
        {'name': 'Billing', 'icon': 'fa-file-invoice-dollar'},
        {'name': 'POS', 'icon': 'fa-cash-register'},
        {'name': 'Settings', 'icon': 'fa-cog'},
    ]

    headers = [
        {'label': 'Code'},
        {'label': 'Product Name'},
        {'label': 'Unit'},
        {'label': 'Current Stock'},
        {'label': 'Sales Scheme', 'sub': ['Deal', 'Free']},
        {'label': 'Purc.Scheme',  'sub': ['Deal', 'Free']},
        {'label': 'Cost Price'},
        {'label': 'Value'},
        {'label': 'M.R.P.'},
        {'label': 'Purchase Price'},
        {'label': 'Sales Price'},
        {'label': 'Company'},
        {'label': 'Manufacturer'},
        {'label': 'Rec.Date'},
        {'label': 'Batch'},
        {'label': 'EXP'},
        {'label': 'Supplier'},
        {'label': 'Inv.No'},
        {'label': 'Inv.Date'},
        {'label': 'Rack No.'},
    ]

    col_fields = [
        'code', 'product_name', 'unit', 'current_stock',
        ['sales_deal', 'sales_free'],
        ['purc_deal', 'purc_free'],
        'cost_price', 'value', 'mrp', 'purchase_price', 'sales_price',
        'company', 'manufacturer', 'rec_date', 'batch', 'exp', 'supplier',
        'inv_no', 'inv_date', 'rack_no',
    ]

    # ---------- SEARCH LOGIC ----------
    search_query = request.GET.get('q', '').strip()
    if search_query:
        stocks = Stock.objects.filter(
            Q(code__icontains=search_query) |
            Q(product_name__icontains=search_query)
        ).order_by('-updated_at')
    else:
        stocks = Stock.objects.all().order_by('-updated_at')[:1000]
    # ----------------------------------

    # ---------- FILE UPLOAD LOGIC ----------
    def norm(s):
        if s is None:
            return ''
        s = str(s).strip().replace('\ufeff', '').replace('\u200b', '')
        return re.sub(r'[^a-z0-9]', '', s.lower())

    mapping = {}
    for h, fld in zip(headers, col_fields):
        if isinstance(h, dict):
            top_label = h.get('label', '')
            sub_labels = h.get('sub') or []
        else:
            top_label = str(h)
            sub_labels = []

        if isinstance(fld, (list, tuple)):
            if sub_labels:
                for sname, fname in zip(sub_labels, fld):
                    mapping[norm(f"{top_label} {sname}")] = fname
            else:
                for idx, fname in enumerate(fld):
                    mapping[norm(f"{top_label}{idx}")] = fname
        else:
            mapping[norm(top_label)] = fld

    mapping.update({
        'productname': 'product_name', 'product': 'product_name',
        'prodname': 'product_name', 'mrp': 'mrp', 'm.r.p': 'mrp',
        'purchaseprice': 'purchase_price', 'salesprice': 'sales_price',
        'costprice': 'cost_price', 'currentstock': 'current_stock',
        'invdate': 'inv_date', 'recdate': 'rec_date', 'expiry': 'exp',
        'expdate': 'exp', 'expirydate': 'exp', 'batchno': 'batch',
        'batchnumber': 'batch', 'suppliername': 'supplier', 'code': 'code',
        'sku': 'code', 'unitcase': 'unit', 'pack': 'unit',
    })

    def read_and_choose_header(uploaded_file):
        data = uploaded_file.read()
        name = getattr(uploaded_file, 'name', '') or ''
        best_df, best_score = None, -1

        def score_columns(cols):
            hits = 0
            for c in cols:
                nc = norm(c)
                if nc in mapping:
                    hits += 1
                else:
                    keys = list(mapping.keys()) + list(set(mapping.values()))
                    if difflib.get_close_matches(nc, keys, n=1, cutoff=0.75):
                        hits += 1
            return hits

        if name.lower().endswith('.csv'):
            for enc in ('utf-8', 'latin1', 'cp1252'):
                try:
                    df = read_csv(BytesIO(data), dtype=object, encoding=enc)
                    sc = score_columns(df.columns)
                    if sc > best_score:
                        best_df, best_score = df, sc
                    break
                except Exception:
                    continue
        else:
            for hr in [0, 1, 2, 3, 4, 5]:
                try:
                    df = read_excel(BytesIO(data), header=hr, engine='openpyxl', dtype=object)
                    sc = score_columns(df.columns)
                    if sc > best_score:
                        best_df, best_score = df, sc
                except Exception:
                    continue
        return best_df, best_score

    # Handle upload
    if request.method == 'POST' and request.FILES.get('inventory_file'):
        uploaded = request.FILES['inventory_file']
        try:
            df, score = read_and_choose_header(uploaded)
        except Exception as e:
            messages.error(request, f"Error reading file: {e}")
            return redirect(request.path)

        if df is None:
            messages.error(request, "Could not parse uploaded spreadsheet.")
            return redirect(request.path)

        numeric_fields = {
            'current_stock', 'sales_deal', 'sales_free',
            'purc_deal', 'purc_free', 'cost_price', 'value',
            'mrp', 'purchase_price', 'sales_price'
        }
        date_fields = {'rec_date', 'inv_date', 'exp'}
        created, updated = 0, 0

        for _, row in df.iterrows():
            data = {}
            for col in df.columns:
                val = row[col]
                if isna(val):
                    val = None
                if val is not None:
                    val = str(val).strip()

                f = mapping.get(norm(col))
                if not f:
                    continue

                if f in numeric_fields:
                    try:
                        data[f] = Decimal(str(val).replace(',', '')) if val else None
                    except Exception:
                        data[f] = None
                elif f in date_fields:
                    try:
                        ts = to_datetime(val, errors='coerce')
                        data[f] = None if isna(ts) else ts.date()
                    except Exception:
                        data[f] = None
                else:
                    data[f] = val

            key_kwargs = {'code': data.get('code')} if data.get('code') else {'product_name': data.get('product_name')}
            if not key_kwargs:
                continue

            obj, created_flag = Stock.objects.update_or_create(defaults=data, **key_kwargs)
            if created_flag:
                created += 1
            else:
                updated += 1

        messages.success(request, f"Upload complete: {created} created, {updated} updated.")
        return redirect(request.path)
    # ---------------------------------------------

    return render(request, 'dashboard/inventory.html', {
        'menu': menu,
        'headers': headers,
        'rows': range(20),
        'stocks': stocks,
        'col_fields': col_fields,
        'search_query': search_query,
    })
