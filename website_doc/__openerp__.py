# -*- coding: utf-8 -*-
{
    'name': 'Website Documentation',
    'category': 'Website',
    'summary': 'Website, Documentation',
    'version': '1.0',
    'description': """
Documentation Using Website, pages and google docs
To create a page you can type: http://localhost:9069/page/asda
        """,
    'author': 'ADHOC SA',
    'depends': [
        'website',
    ],
    'data': [
        'data/doc_data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/doc.xml',
        'views/website_doc.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/website_doc.xml'
    ],
    'installable': True,
    'application': True,
}
