# dashboard/context_processors.py

def sidebar_menu(request):
    """
    Provides sidebar menu globally to all templates.
    """
    menu = [
        {"name": "Sales", "icon": "fa-cart-plus", "url": "/sales-entry/"},
        {"name": "Purchase", "icon": "fa-truck", "url": "/purchase/"},
        {"name": "Inventory", "icon": "fa-boxes", "url": "/inventory/"},
        {"name": "Accounts", "icon": "fa-wallet", "url": "/accounts/"},
        {"name": "Reports", "icon": "fa-chart-line", "url": "/reports/"},
        {"name": "Masters", "icon": "fa-database", "url": "/masters/"},
        {"name": "Billing", "icon": "fa-file-invoice-dollar", "url": "/billing/"},
        {"name": "POS", "icon": "fa-cash-register", "url": "/pos/"},
        {"name": "Setting", "icon": "fa-cog", "url": "/setting/"},
    ]
    return {'menu': menu}
