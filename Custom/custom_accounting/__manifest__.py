{
    'name': "Custom Accounts",
    'version': '1.0',
    'depends': ['base'],
    'author': "Ali",
    'category': 'Accounting/Accounting',
    'application': True,
    'auto_install': False,
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/default.xml',
        'models/sequences.xml',
    ],
}
