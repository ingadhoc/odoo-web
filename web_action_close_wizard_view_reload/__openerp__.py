{
    'name': 'Reload view on window close Action',
    'category': 'Web',
    'version': '8.0.1.0.1',
    'description': """
Reload view on window close Action
==================================
Makes ir_actions_act_window_close to reload kanban or tree view
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
    'installable': False,
    'auto_install': False,
}
