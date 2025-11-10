# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import http
from odoo.http import request


class AppLauncherHome(http.Controller):

    def _get_custom_icon_path(self, app_name):
        """Map app names to custom icon files."""
        icon_mapping = {
            'sales': '/app_launcher_home/static/src/img/icons/icon_sales.svg',
            'crm': '/app_launcher_home/static/src/img/icons/icon_crm.svg',
            'invoicing': '/app_launcher_home/static/src/img/icons/icon_accounting.svg',
            'accounting': '/app_launcher_home/static/src/img/icons/icon_accounting.svg',
            'inventory': '/app_launcher_home/static/src/img/icons/icon_inventory.svg',
            'purchase': '/app_launcher_home/static/src/img/icons/icon_purchase.svg',
            'hr': '/app_launcher_home/static/src/img/icons/icon_hr.svg',
            'employees': '/app_launcher_home/static/src/img/icons/icon_hr.svg',
            'account': '/app_launcher_home/static/src/img/icons/icon_accounting.svg',
        }

        app_name_lower = app_name.lower()
        for key, path in icon_mapping.items():
            if key in app_name_lower:
                return path
        return None

    def _get_icon_svg(self, app_name):
        """Generate a beautiful SVG icon based on the app name."""
        # Icon definitions with Oravex color scheme
        icons = {
            'discuss': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/>'
            },
            'calendar': {
                'color': '#0d7c88',
                'bg': '#e0f7f8',
                'icon': '<path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>'
            },
            'contacts': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M16.5 12c1.38 0 2.49-1.12 2.49-2.5S17.88 7 16.5 7 14 8.12 14 9.5s1.12 2.5 2.5 2.5zM9 11c1.66 0 2.99-1.34 2.99-3S10.66 5 9 5C7.34 5 6 6.34 6 8s1.34 3 3 3zm7.5 3c-1.83 0-5.5.92-5.5 2.75V19h11v-2.25c0-1.83-3.67-2.75-5.5-2.75zM9 13c-2.33 0-7 1.17-7 3.5V19h7v-2.25c0-.85.33-2.34 2.37-3.47C10.5 13.1 9.66 13 9 13z"/>'
            },
            'crm': {
                'color': '#1a4d6d',
                'bg': '#e0f2f8',
                'icon': '<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>'
            },
            'sales': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/>'
            },
            'invoicing': {
                'color': '#0d7c88',
                'bg': '#e0f7f8',
                'icon': '<path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>'
            },
            'accounting': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>'
            },
            'inventory': {
                'color': '#1a4d6d',
                'bg': '#e0f2f8',
                'icon': '<path d="M20 2H4c-1 0-2 .9-2 2v3.01c0 .72.43 1.34 1 1.69V20c0 1.1 1.1 2 2 2h14c.9 0 2-.9 2-2V8.7c.57-.35 1-.97 1-1.69V4c0-1.1-1-2-2-2zm-5 12H9v-2h6v2zm5-7H4V4h16v3z"/>'
            },
            'purchase': {
                'color': '#0d7c88',
                'bg': '#e0f7f8',
                'icon': '<path d="M17 18c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2zM7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zm0-3l1.1-2h7.45c.75 0 1.41-.41 1.75-1.03L21.7 4H5.21l-.94-2H1v2h2l3.6 7.59L3.25 17H19v-2H7z"/>'
            },
            'point of sale': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M17 2H7c-1.1 0-2 .9-2 2v2c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 4H7V4h10v2zm3 16H4v-2h16v2zm0-4H4v-6h16v6zM9 12h6v2H9v-2z"/>'
            },
            'project': {
                'color': '#1a4d6d',
                'bg': '#e0f2f8',
                'icon': '<path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>'
            },
            'employees': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>'
            },
            'hr': {
                'color': '#0d7c88',
                'bg': '#e0f7f8',
                'icon': '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>'
            },
            'website': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-5 14H4v-4h11v4zm0-5H4V9h11v4zm5 5h-4V9h4v9z"/>'
            },
            'dashboards': {
                'color': '#1a4d6d',
                'bg': '#e0f2f8',
                'icon': '<path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>'
            },
            'settings': {
                'color': '#0d7c88',
                'bg': '#e0f7f8',
                'icon': '<path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>'
            },
            'mail': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>'
            },
            'apps': {
                'color': '#1a4d6d',
                'bg': '#e0f2f8',
                'icon': '<path d="M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"/>'
            },
            'account': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>'
            },
            'default': {
                'color': '#0ea5b5',
                'bg': '#e0f7f8',
                'icon': '<path d="M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"/>'
            }
        }

        # Find matching icon
        app_name_lower = app_name.lower()
        icon_data = icons.get(app_name_lower, icons['default'])

        # Generate SVG with proper positioning
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="72" height="72">
            <circle cx="32" cy="32" r="30" fill="{icon_data['bg']}"/>
            <g transform="translate(32, 32)">
                <g transform="translate(-12, -12)">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="{icon_data['color']}">
                        {icon_data['icon']}
                    </svg>
                </g>
            </g>
        </svg>'''

        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

    @http.route('/web/app_launcher', type='http', auth='user')
    def app_launcher(self, **kwargs):
        """Display the app launcher home page with all available apps."""
        # Get all top-level menus (these represent the main apps)
        IrUiMenu = request.env['ir.ui.menu']

        menus = IrUiMenu.search([('parent_id', '=', False)], order='sequence,name')

        app_data = []
        for menu in menus:
            # First try to use custom uploaded icons
            custom_icon_path = self._get_custom_icon_path(menu.name)

            if custom_icon_path:
                icon_path = custom_icon_path
            else:
                # Fall back to generated SVG icons
                icon_path = self._get_icon_svg(menu.name)

            app_info = {
                'id': menu.id,
                'name': menu.name,
                'icon': icon_path,
                'menu_id': menu.id,
                'action_id': menu.action.id if menu.action else False,
            }
            app_data.append(app_info)

        return request.render('app_launcher_home.app_launcher_page', {
            'apps': app_data,
            'company_name': request.env.company.name,
        })
