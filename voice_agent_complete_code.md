# Complete Voice Agent Integration Code

## All Files Needed for LiveKit Voice Agent + Odoo Integration

---

## 1. Odoo Module: `__init__.py`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/__init__.py`

```python
from . import controllers
from . import models
```

---

## 2. Odoo Module: `__manifest__.py`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/__manifest__.py`

```python
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
```

---

## 3. Controllers: `__init__.py`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/controllers/__init__.py`

```python
from . import main
```

---

## 4. Controllers: `main.py`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/controllers/main.py`

```python
import json
import logging
import time
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
            # Get LiveKit credentials from config or environment
            livekit_url = "wss://live-agent-9pacbr1x.livekit.cloud"
            livekit_api_key = "APIGXGkGsm32tQF"
            livekit_api_secret = "RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA"

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
```

---

## 5. Models: `__init__.py`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/models/__init__.py`

```python
# No models needed for now - placeholder for future extensions
```

---

## 6. JavaScript: `voice_widget.js`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/static/src/js/voice_widget.js`

```javascript
/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class VoiceWidget extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            isConnected: false,
            isRecording: false,
            isSpeaking: false,
            error: null,
        });

        this.room = null;
        this.localParticipant = null;

        onMounted(() => {
            this.loadLiveKitSDK();
        });

        onWillUnmount(() => {
            this.disconnect();
        });
    }

    async loadLiveKitSDK() {
        // Load LiveKit Client SDK from CDN
        if (window.LivekitClient) {
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://unpkg.com/livekit-client@2.0.0/dist/livekit-client.umd.min.js';
        script.onload = () => {
            console.log('LiveKit SDK loaded');
        };
        script.onerror = () => {
            this.state.error = 'Failed to load LiveKit SDK';
        };
        document.head.appendChild(script);
    }

    async connect() {
        try {
            this.state.error = null;

            // Get token from Odoo backend
            const tokenData = await this.rpc('/voice_agent/get_token', {});

            if (tokenData.error) {
                throw new Error(tokenData.error);
            }

            // Connect to LiveKit room
            const LivekitClient = window.LivekitClient;
            this.room = new LivekitClient.Room({
                adaptiveStream: true,
                dynacast: true,
            });

            // Set up event listeners
            this.room.on('connected', () => {
                console.log('Connected to LiveKit room');
                this.state.isConnected = true;
            });

            this.room.on('disconnected', () => {
                console.log('Disconnected from LiveKit');
                this.state.isConnected = false;
                this.state.isRecording = false;
                this.state.isSpeaking = false;
            });

            this.room.on('dataReceived', (payload, participant) => {
                this.handleNavigationMessage(payload);
            });

            // Connect to room
            await this.room.connect(tokenData.url, tokenData.token);

            // Enable microphone
            await this.room.localParticipant.setMicrophoneEnabled(true);
            this.state.isRecording = true;

        } catch (error) {
            console.error('Connection error:', error);
            this.state.error = error.message;
        }
    }

    async disconnect() {
        if (this.room) {
            await this.room.disconnect();
            this.room = null;
        }
        this.state.isConnected = false;
        this.state.isRecording = false;
        this.state.isSpeaking = false;
    }

    async toggleConnection() {
        if (this.state.isConnected) {
            await this.disconnect();
        } else {
            await this.connect();
        }
    }

    handleNavigationMessage(payload) {
        try {
            const decoder = new TextDecoder();
            const message = JSON.parse(decoder.decode(payload));

            if (message.type === 'agent-navigation-url') {
                // Navigate to the specified path
                window.dispatchEvent(new CustomEvent('voice-navigate', {
                    detail: { pathname: message.pathname }
                }));
            }
        } catch (error) {
            console.error('Error handling navigation message:', error);
        }
    }
}

VoiceWidget.template = "odoo_voice_agent.VoiceWidget";

// Register the widget in the systray
export const systrayItem = {
    Component: VoiceWidget,
};

registry.category("systray").add("VoiceWidget", systrayItem, { sequence: 1 });
```

---

## 7. JavaScript: `navigation_handler.js`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/static/src/js/navigation_handler.js`

```javascript
/** @odoo-module **/

import { browser } from "@web/core/browser/browser";

// Listen for voice navigation events
window.addEventListener('voice-navigate', (event) => {
    const { pathname } = event.detail;

    if (pathname) {
        console.log('Voice navigation to:', pathname);

        // Use Odoo's router to navigate
        browser.location.hash = pathname;

        // Alternatively, reload with new hash
        // window.location.href = window.location.origin + pathname;
    }
});

// Send current location to voice agent (if connected)
function sendCurrentLocation() {
    const currentHash = window.location.hash;

    // This would be called when agent asks "where am I?"
    // Implementation depends on how we send messages back to agent
    console.log('Current location:', currentHash);
}

// Export for use in other modules
export { sendCurrentLocation };
```

---

## 8. CSS: `voice_widget.css`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/static/src/css/voice_widget.css`

```css
.voice-widget-container {
    position: relative;
}

.voice-widget-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.voice-widget-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.voice-widget-button.active {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    animation: pulse 2s infinite;
}

.voice-widget-button.speaking {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    animation: speaking-pulse 0.8s infinite;
}

.voice-widget-icon {
    width: 24px;
    height: 24px;
    fill: white;
}

.voice-widget-status {
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10b981;
    border: 2px solid white;
}

.voice-widget-status.disconnected {
    background: #ef4444;
}

.voice-widget-status.recording {
    background: #f59e0b;
    animation: blink 1s infinite;
}

.voice-error {
    position: absolute;
    bottom: 50px;
    right: 0;
    background: #fee2e2;
    color: #991b1b;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    white-space: nowrap;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

@keyframes speaking-pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

@keyframes blink {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.3;
    }
}
```

---

## 9. XML Templates: `voice_widget_templates.xml`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/static/src/xml/voice_widget_templates.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">

    <t t-name="odoo_voice_agent.VoiceWidget" owl="1">
        <div class="voice-widget-container">
            <button
                class="voice-widget-button"
                t-att-class="{
                    'active': state.isRecording,
                    'speaking': state.isSpeaking
                }"
                t-on-click="toggleConnection"
                title="Voice Navigation Assistant">

                <!-- Microphone Icon -->
                <svg class="voice-widget-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>

                <!-- Status Indicator -->
                <div
                    class="voice-widget-status"
                    t-att-class="{
                        'disconnected': !state.isConnected,
                        'recording': state.isRecording
                    }">
                </div>
            </button>

            <!-- Error Message -->
            <div t-if="state.error" class="voice-error">
                <t t-esc="state.error"/>
            </div>
        </div>
    </t>

</templates>
```

---

## 10. Views: `webclient_templates.xml`

**Location:** `/opt/odoo/custom_addons/odoo_voice_agent/views/webclient_templates.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- No additional templates needed - widget is registered via JS -->
    </data>
</odoo>
```

---

## 11. Updated Agent.py Navigation Functions

**Location:** `/opt/livekit-agent/agent.py`

**Add these navigation functions (replace lines 223-420):**

```python
# Odoo Navigation Functions
@function_tool
async def navigate_to_sales(self, context: RunContext):
    """Navigate to Sales module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=sales.sale_menu_root"
    await self._send_navigation_url(context, url)
    return "Opening Sales module"

@function_tool
async def navigate_to_crm(self, context: RunContext):
    """Navigate to CRM/Customers module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=crm.crm_menu_root"
    await self._send_navigation_url(context, url)
    return "Opening CRM module"

@function_tool
async def navigate_to_inventory(self, context: RunContext):
    """Navigate to Inventory/Stock module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=stock.menu_stock_root"
    await self._send_navigation_url(context, url)
    return "Opening Inventory module"

@function_tool
async def navigate_to_accounting(self, context: RunContext):
    """Navigate to Accounting module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=account.menu_finance"
    await self._send_navigation_url(context, url)
    return "Opening Accounting module"

@function_tool
async def navigate_to_purchases(self, context: RunContext):
    """Navigate to Purchases module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=purchase.menu_purchase_root"
    await self._send_navigation_url(context, url)
    return "Opening Purchases module"

@function_tool
async def navigate_to_hr(self, context: RunContext):
    """Navigate to Human Resources module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=hr.menu_hr_root"
    await self._send_navigation_url(context, url)
    return "Opening HR module"

@function_tool
async def navigate_to_projects(self, context: RunContext):
    """Navigate to Projects module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=project.menu_main_pm"
    await self._send_navigation_url(context, url)
    return "Opening Projects module"

@function_tool
async def navigate_to_manufacturing(self, context: RunContext):
    """Navigate to Manufacturing/MRP module"""
    url = f"{FRONTEND_BASE_URL}/web#menu_id=mrp.menu_mrp_root"
    await self._send_navigation_url(context, url)
    return "Opening Manufacturing module"

@function_tool
async def go_home(self, context: RunContext):
    """Navigate to home/dashboard"""
    url = f"{FRONTEND_BASE_URL}/web"
    await self._send_navigation_url(context, url)
    return "Going to home page"

@function_tool
async def where_am_i(self, context: RunContext):
    """Tell user their current location - they need to inform you"""
    return "I need you to tell me where you are. What page or module are you currently viewing?"

async def _send_navigation_url(self, context: RunContext, url: str):
    """Helper to send navigation URL via data channel"""
    try:
        # Extract just the path part
        from urllib.parse import urlparse
        parsed = urlparse(url)
        pathname = parsed.fragment if parsed.fragment else parsed.path

        # Send via data channel
        navigation_data = {
            "type": "agent-navigation-url",
            "pathname": f"#{pathname}" if not pathname.startswith('#') else pathname
        }

        # Send to room
        if hasattr(self, '_room') and self._room:
            await self._room.local_participant.publish_data(
                json.dumps(navigation_data).encode('utf-8'),
                reliable=True
            )
    except Exception as e:
        logger.error(f"Error sending navigation: {e}")
```

---

## 12. Systemd Service File

**Location:** `/etc/systemd/system/livekit-agent.service`

```ini
[Unit]
Description=LiveKit Voice Agent for Odoo
Documentation=https://docs.livekit.io/agents
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/livekit-agent
Environment=PATH=/opt/livekit-agent/venv/bin
ExecStart=/opt/livekit-agent/venv/bin/python agent.py start
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## Installation Instructions

### Step 1: Upload All Files to Server

```bash
# From your Windows machine, upload the module
scp -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" -r odoo_voice_agent/ ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/tmp/

# Then SSH and move to Odoo
ssh -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com
sudo mv /tmp/odoo_voice_agent /opt/odoo/custom_addons/
sudo chown -R odoo:odoo /opt/odoo/custom_addons/odoo_voice_agent
```

### Step 2: Install LiveKit Python SDK in Odoo Environment

```bash
sudo /usr/bin/python3.11 -m pip install livekit livekit-api
```

### Step 3: Create Systemd Service

```bash
sudo nano /etc/systemd/system/livekit-agent.service
# Paste the content from section 12 above

sudo systemctl daemon-reload
sudo systemctl enable livekit-agent
sudo systemctl start livekit-agent
sudo systemctl status livekit-agent
```

### Step 4: Restart Odoo

```bash
sudo systemctl restart odoo
```

### Step 5: Install Module in Odoo

1. Go to http://51.20.91.45:8069
2. Login
3. Go to Apps menu
4. Click "Update Apps List"
5. Search for "Voice Navigation"
6. Click Install

### Step 6: Test

1. Click the microphone button in the top-right systray
2. Allow microphone permissions
3. Say "افتح المبيعات" (Open Sales) or "Open sales"
4. Watch Odoo navigate to the Sales module!

---

## Troubleshooting

### Check LiveKit Agent Logs
```bash
sudo journalctl -u livekit-agent -f
```

### Check Odoo Logs
```bash
sudo tail -f /var/log/odoo/odoo.log
```

### Check Browser Console
Press F12 in browser and check for JavaScript errors

---

## Security Notes

**IMPORTANT:** The LiveKit credentials in `main.py` are hardcoded for simplicity. For production:

1. Move credentials to Odoo system parameters
2. Or use environment variables
3. Implement proper access control
4. Use HTTPS
5. Revoke the old GitHub token in .env

---

## Next Steps

1. Customize agent personality in `/opt/livekit-agent/prompts/agent_instructions.txt`
2. Add more navigation functions for your specific Odoo modules
3. Implement advanced features (create records, search data, etc.)
4. Add proper error handling and user feedback
5. Style the widget to match your Odoo theme

---

**End of Complete Code Guide**
