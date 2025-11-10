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
