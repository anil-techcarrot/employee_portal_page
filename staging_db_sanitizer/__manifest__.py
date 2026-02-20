{
    'name': 'Staging Database Sanitizer',
    'version': '19.0.0',
    # 'category': 'Tools',
    'summary': 'Automatically sanitize production data in staging environment',
    'description': """
        This module automatically sanitizes sensitive production data when
        restored to staging environment. It runs once per restore and logs
        all operations.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_data.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}