{
    'name': 'Website Issue',
    'category': 'Website',
    'website': 'www.ingadhoc.com',
    'summary': 'Create Issues From a Website Form',
    'version': '1.0',
    'description': """
Website Issue
=============
        """,
    'author': 'Ing ADHOC',
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
