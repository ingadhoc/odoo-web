{
    'name': 'Hardware Collector',
    'category': '',
    'version': '9.0.1.0.0',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'description':
        '''
Creates a Widget that will connect to a HW interface
It can be added in any Float field on formview with: 'widget="hw_collector"'
You need to add an ir parameter with key 'hw.proxy' and value url where to read.
        ''',
    'depends': ['web'],
    'css': [],
    'data': [
        'views/web_hw_collector.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': False,
    'auto_install': False,
}
