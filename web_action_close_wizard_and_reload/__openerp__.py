{
    'name': 'Web Action, close wizard and reload',
    'category': 'Web',
    'version': '8.0.1.0.0',
    'description': """
Web Action, close wizard and reload
===================================
TODO: tal vez podemos modificar directamente ir_actions_act_window_close
para que se comporte asi
        """,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': [
        'web',
    ],
    'data': [
        'view/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
