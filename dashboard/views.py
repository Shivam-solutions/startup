from django.shortcuts import render

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


def sales_entry(request):
    # Keep the same menu so the sidebar stays consistent
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
    # Render 20 empty table rows (visual placeholder like the image)
    rows = range(20)
    return render(request, 'dashboard/sales_entry.html', {
        'menu': menu,
        'rows': rows
    })


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

def inventory(request):
    from django.shortcuts import render, redirect
    from django.contrib import messages
    import re, difflib
    from decimal import Decimal, InvalidOperation
    from io import BytesIO

    # Menu + headers (same as template expects)
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

    # normalizer
    def norm(s):
        if s is None:
            return ''
        s = str(s)
        s = s.strip().replace('\ufeff', '').replace('\u200b', '')
        return re.sub(r'[^a-z0-9]', '', s.lower())

    # build mapping (normalized header -> field)
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
                    mapping[norm(sname)] = fname
                    mapping[norm(f"{top_label}_{sname}")] = fname
                    mapping[norm(f"{top_label}-{sname}")] = fname
            else:
                for idx, fname in enumerate(fld):
                    mapping[norm(f"{top_label}{idx}")] = fname
        else:
            mapping[norm(top_label)] = fld

    # manual synonyms
    mapping.update({
        'productname':'product_name', 'product':'product_name', 'prodname':'product_name',
        'mrp':'mrp', 'm.r.p':'mrp', 'purchaseprice':'purchase_price',
        'salesprice':'sales_price', 'costprice':'cost_price',
        'currentstock':'current_stock', 'invdate':'inv_date', 'recdate':'rec_date',
        'expiry':'exp', 'expdate':'exp', 'expirydate':'exp', 'batchno':'batch',
        'batchnumber':'batch', 'suppliername':'supplier', 'code':'code', 'sku':'code',
        'unitcase':'unit', 'pack':'unit',
    })

    # read uploaded file with intelligent header-row scoring
    def read_and_choose_header(uploaded_file):
        import pandas as pd
        data = uploaded_file.read()
        name = getattr(uploaded_file, 'name', '') or ''
        # candidate header rows to try
        header_candidates = [0, 1, 2, 3, 4, 5]
        best_df = None
        best_score = -1
        best_header_row = None
        best_col_names = None

        # helper scoring based on mapping matches
        def score_columns(cols):
            hits = 0
            for c in cols:
                nc = norm(c)
                if nc in mapping or nc in mapping.values():
                    hits += 1
                else:
                    # fuzzy attempt
                    # compare nc with mapping keys and mapping values
                    keys = list(mapping.keys()) + list(set(mapping.values()))
                    match = difflib.get_close_matches(nc, keys, n=1, cutoff=0.75)
                    if match:
                        hits += 1
            return hits

        try_csv = str(name).lower().endswith('.csv')
        if try_csv:
            # try csv read
            for enc in ('utf-8', 'latin1', 'cp1252'):
                try:
                    df = pd.read_csv(BytesIO(data), dtype=object, encoding=enc)
                    cols = list(df.columns)
                    sc = score_columns(cols)
                    if sc > best_score:
                        best_score = sc
                        best_df = df
                        best_header_row = 0
                        best_col_names = cols
                    break
                except Exception:
                    continue
        else:
            # try the set of header rows
            for hr in header_candidates:
                try:
                    df = pd.read_excel(BytesIO(data), header=hr, engine='openpyxl', dtype=object)
                except Exception:
                    try:
                        df = pd.read_excel(BytesIO(data), header=hr, dtype=object)
                    except Exception:
                        df = None
                if df is None:
                    continue
                cols = list(df.columns)
                sc = score_columns(cols)
                # prefer header rows that produce more matches
                if sc > best_score:
                    best_score = sc
                    best_df = df
                    best_header_row = hr
                    best_col_names = cols

            # fallback: try header=None and set first row as header
            if best_df is None or best_score <= 0:
                try:
                    df_raw = pd.read_excel(BytesIO(data), header=None, engine='openpyxl', dtype=object)
                except Exception:
                    try:
                        df_raw = pd.read_excel(BytesIO(data), header=None, dtype=object)
                    except Exception:
                        df_raw = None
                if df_raw is not None and len(df_raw) > 0:
                    first_row = df_raw.iloc[0].tolist()
                    df_raw.columns = first_row
                    df = df_raw.iloc[1:].reset_index(drop=True)
                    cols = list(df.columns)
                    sc = score_columns(cols)
                    if sc > best_score:
                        best_score = sc
                        best_df = df
                        best_header_row = 'first-row-as-header'
                        best_col_names = cols

        return best_df, best_header_row, best_score, best_col_names

    # POST processing
    if request.method == 'POST' and request.FILES.get('inventory_file'):
        try:
            import pandas as pd
        except Exception:
            messages.error(request, 'pandas and openpyxl are required for Excel upload. Install them and retry.')
            return redirect(request.path)

        f = request.FILES['inventory_file']
        try:
            df, detected_header_row, score, col_names = read_and_choose_header(f)
        except Exception as e:
            messages.error(request, f'Failed to read uploaded file: {e}')
            return redirect(request.path)

        if df is None:
            messages.error(request, 'Could not parse uploaded spreadsheet.')
            return redirect(request.path)

        # flatten multiindex columns if any
        try:
            if hasattr(df.columns, 'levels') and len(getattr(df.columns, 'levels', [])) > 1:
                df.columns = [' '.join([str(x) for x in tup if str(x) != 'nan']).strip() for tup in df.columns.values]
        except Exception:
            pass

        uploaded_cols = [str(c) for c in df.columns.tolist()]

        # Build col_map using normalized exact match and fuzzy match (similar to previous logic)
        col_map = {}
        unmapped = []
        keys_for_match = list(mapping.keys()) + list(set(mapping.values()))
        for c in uploaded_cols:
            nc = norm(c)
            if nc in mapping:
                col_map[c] = mapping[nc]
                continue
            if nc in mapping.values():
                col_map[c] = nc
                continue
            best = difflib.get_close_matches(nc, keys_for_match, n=1, cutoff=0.7)
            if best:
                bk = best[0]
                if bk in mapping:
                    col_map[c] = mapping[bk]
                else:
                    col_map[c] = bk
            else:
                # looser ratio attempt
                best_ratio = 0.0
                best_key = None
                for mk in keys_for_match:
                    r = difflib.SequenceMatcher(None, nc, mk).ratio()
                    if r > best_ratio:
                        best_ratio = r
                        best_key = mk
                if best_ratio >= 0.5:
                    if best_key in mapping:
                        col_map[c] = mapping[best_key]
                    else:
                        col_map[c] = best_key
                else:
                    unmapped.append(c)

        # avoid collisions (keep first mapping)
        final_col_map = {}
        used_fields = set()
        collisions = {}
        for dfcol, fld in col_map.items():
            if fld in used_fields:
                collisions.setdefault(fld, []).append(dfcol)
            else:
                final_col_map[dfcol] = fld
                used_fields.add(fld)
        for fld, extras in collisions.items():
            for ex in extras:
                unmapped.append(ex)

        if not final_col_map:
            # helpful debug info
            messages.error(request, 'No recognizable columns found in uploaded file. Check header names.')
            messages.info(request, f'Detected header row: {detected_header_row} (score={score}). Uploaded columns: {", ".join(uploaded_cols[:30])}')
            return redirect(request.path)

        # Save rows to DB
        from .models import Stock
        numeric_fields = {'current_stock','sales_deal','sales_free','purc_deal','purc_free',
                          'cost_price','value','mrp','purchase_price','sales_price'}
        date_fields = {'rec_date','inv_date','exp'}
        created = 0
        updated = 0

        for _, row in df.iterrows():
            data = {}
            for dfcol, fld in final_col_map.items():
                try:
                    val = row[dfcol]
                except Exception:
                    val = None
                # pandas NA handling
                try:
                    import pandas as _pd
                    if _pd.isna(val):
                        val = None
                except Exception:
                    pass

                if fld in numeric_fields:
                    if val is None:
                        data[fld] = None
                    else:
                        sval = str(val).replace(',', '').strip()
                        try:
                            data[fld] = Decimal(sval)
                        except Exception:
                            try:
                                data[fld] = Decimal(float(sval))
                            except Exception:
                                data[fld] = None
                elif fld in date_fields:
                    if val is None:
                        data[fld] = None
                    else:
                        try:
                            import pandas as _pd
                            ts = _pd.to_datetime(val, errors='coerce')
                            data[fld] = None if _pd.isna(ts) else ts.date()
                        except Exception:
                            data[fld] = None
                else:
                    data[fld] = None if val is None else str(val).strip()

            # choose unique key
            key_kwargs = {}
            if data.get('code'):
                key_kwargs['code'] = data['code']
            elif data.get('product_name'):
                key_kwargs['product_name'] = data['product_name']
            else:
                continue

            try:
                obj, created_flag = Stock.objects.update_or_create(defaults=data, **key_kwargs)
                if created_flag:
                    created += 1
                else:
                    updated += 1
            except Exception:
                continue

        matched = [f"{dfcol} -> {fld}" for dfcol, fld in final_col_map.items()]
        if matched:
            messages.success(request, f'Upload processed. Created: {created}, Updated: {updated}.')
            messages.info(request, 'Mapped columns: ' + '; '.join(matched))
        if unmapped:
            messages.warning(request, 'Unmapped columns (ignored): ' + ', '.join(unmapped[:50]))

        messages.info(request, f'Detected header row: {detected_header_row}, score: {score}')
        return redirect(request.path)

    # GET: show existing stocks (or placeholders)
    try:
        from .models import Stock
        stocks = Stock.objects.all().order_by('-updated_at')[:1000]
    except Exception:
        stocks = []

    return render(request, 'dashboard/inventory.html', {
        'menu': menu,
        'headers': headers,
        'rows': range(20),
        'stocks': stocks,
        'col_fields': col_fields,
    })
