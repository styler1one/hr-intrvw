// API Configuration for Vercel deployment
// Change this to your Vercel domain after deployment
const API_CONFIG = {
    // For local development with Vercel CLI
    BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:3000'
        : window.location.origin,
    
    // Polling interval for chat updates (in milliseconds)
    POLL_INTERVAL: 2000,
    
    // Timeout for API requests (in milliseconds)
    REQUEST_TIMEOUT: 30000
};

// Export for use in main app
window.API_CONFIG = API_CONFIG;
