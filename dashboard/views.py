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
