{
    'name': 'Website Issue',
    'category': 'Website',
    'summary': 'Create Issues From a Website Form',
    'version': '8.0.1.0.0',
    'description': """
Website Issue
=============
        """,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': [
        'website_partner',
        'project_issue',
        ],
    'data': [
        'data/website_issue_data.xml',
        'views/website_issue.xml',
        'views/snippets.xml',
    ],
    'installable': True,
    'auto_install': False,
}
