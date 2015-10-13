{
    'name': 'Login Serial',
    'category': 'Login Serial',
    'summary': 'Login Serial',
    'version': '9.0.1.0.0',
    'description': '''
Adds a Serial Id field to the users that can be used to login in without a
password.

A new URL is provided "http://domain/login_serial/" to login with the specified
Serial Id.''',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'depends': ['website'],
    'external_dependencies':
    {
    },
    'data':
    [
        'views/res_users_view.xml',
        'views/webclient_templates.xml',
    ],
    'installable': False,
}
