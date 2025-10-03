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
        {'title':'Stock Value','value':'₹ 4,12,300'},
        {'title':'Receivables','value':'₹ 2,05,400'},
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
