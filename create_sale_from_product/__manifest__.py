# -*- coding: utf-8 -*-
{
    'name': "Create Sale Order From Product",
    'version': '19.0.0.1.0',
    'category': 'Sales',
    'author': "Mayank",
    'license': 'LGPL-3',
    "support": "odoodevelopmentpartner@gmail.com",
    'summary': 'Create Sale Orders directly from selected products',
    'depends': ['base', 'sale_management', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_sale_wizard_view.xml',
        'views/product_action.xml',
    ],
    'images': [
        "static/description/banner.png",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
