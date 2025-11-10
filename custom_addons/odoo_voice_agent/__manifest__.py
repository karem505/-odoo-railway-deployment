{
    'name': 'Odoo Voice Navigation Agent',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Voice-controlled navigation using LiveKit AI Agent',
    'description': '''
        Voice Navigation Assistant for Odoo
        ====================================
        * Navigate between modules using voice commands
        * Bilingual support (Arabic/English)
        * Floating voice widget on all pages
        * Powered by LiveKit and OpenAI
    ''',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_voice_agent/static/src/js/voice_widget.js',
            'odoo_voice_agent/static/src/js/navigation_handler.js',
            'odoo_voice_agent/static/src/css/voice_widget.css',
            'odoo_voice_agent/static/src/xml/voice_widget_templates.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
