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
