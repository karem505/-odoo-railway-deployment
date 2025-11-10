import json
import logging
import time
import os
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from livekit import api
except ImportError:
    _logger.warning("LiveKit SDK not installed. Install with: pip install livekit")
    api = None


class VoiceAgentController(http.Controller):

    @http.route('/voice_agent/get_token', type='json', auth='user')
    def get_livekit_token(self, **kwargs):
        """Generate LiveKit access token for the current user"""
        if not api:
            return {'error': 'LiveKit SDK not installed'}

        try:
            # Get LiveKit credentials from environment variables (Railway)
            livekit_url = os.getenv('LIVEKIT_URL', 'wss://live-agent-9pacbr1x.livekit.cloud')
            livekit_api_key = os.getenv('LIVEKIT_API_KEY', 'APIGXGkGsm32tQF')
            livekit_api_secret = os.getenv('LIVEKIT_API_SECRET', 'RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA')

            # Generate unique room name for this user
            user = request.env.user
            room_name = f"odoo_voice_{user.id}_{int(time.time())}"
            participant_name = user.name or f"User{user.id}"

            # Create access token
            token = api.AccessToken(livekit_api_key, livekit_api_secret)
            token.with_identity(participant_name).with_name(participant_name).with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,
                    can_publish=True,
                    can_subscribe=True,
                )
            )

            jwt_token = token.to_jwt()

            return {
                'token': jwt_token,
                'url': livekit_url,
                'room': room_name,
                'participant': participant_name,
            }

        except Exception as e:
            _logger.error(f"Error generating LiveKit token: {str(e)}")
            return {'error': str(e)}

    @http.route('/voice_agent/get_modules', type='json', auth='user')
    def get_installed_modules(self, **kwargs):
        """Return list of installed Odoo modules with their menu IDs"""
        try:
            # Get all menu items accessible to current user
            menus = request.env['ir.ui.menu'].search([])

            modules_list = []
            for menu in menus:
                if menu.parent_id:  # Skip root menus
                    continue

                modules_list.append({
                    'id': menu.id,
                    'name': menu.name,
                    'xml_id': menu.get_xml_id().get(menu.id, ''),
                    'action': menu.action.id if menu.action else None,
                    'web_icon': menu.web_icon,
                })

            return {'modules': modules_list}

        except Exception as e:
            _logger.error(f"Error fetching modules: {str(e)}")
            return {'error': str(e)}
