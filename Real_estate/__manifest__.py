{
    'name': 'Real_estate',
    'application': True,
    'installble': True,
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/wizard_view.xml',
        'views/estate_menu.xml',
        'views/estate_view.xml',
        # 'views/menu.xml',
        'data/estate_data.xml',
        'views/estate_templets.xml',
    ],
    'license': 'LGPL-3',
}
