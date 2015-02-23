{
    'name': 'Hardware Collector',
    'category': '',
    'version': '1.0',
    'author': 'IngAdhoc',
    'description':
        '''
Creates a Widget that will connect to a HW interface
        ''',
    'depends': ['product', 'web'],
    'css': [],
    'data': [
        'views/web_hw_collector.xml',
        'product_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
}
