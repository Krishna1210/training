{
    'name': 'Real_estate',
    'application': True,
    'installble': True,
    'depends': ['website' , 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/wizard_view.xml',
        'views/estate_menu.xml',
        'views/estate_view.xml',
        'views/form.xml',
        'data/estate_data.xml',
        'views/estate_templets.xml',
        'views/report_template.xml',
        'views/report.xml',
    ],
    'license': 'LGPL-3',
}
