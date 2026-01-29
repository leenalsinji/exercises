{
    'name': 'Real Estate',
    'category': 'Services',
    'application': True,

    'depends': ['base', 'web', 'crm'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_dashboard_views.xml',
        'report/estate_property_reports.xml',   
        'report/estate_property_templates.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
'assets': {
    'web.assets_backend': [
        'estate/static/src/**/*', 
    ],
},
}
