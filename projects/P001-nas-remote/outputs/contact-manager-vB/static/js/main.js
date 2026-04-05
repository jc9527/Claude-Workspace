/**
 * Contact Manager vB - Main JavaScript
 */

// Global error handler for fetch
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
});

// Add CSRF token handling if needed
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

// Utility function for API calls
async function apiCall(url, method, body = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (body && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(body);
    }
    
    const response = await fetch(url, options);
    return response;
}

// Format date helper
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW');
}

// Toast notification helper (if needed)
function showToast(message, type = 'info') {
    // Can be implemented with Bootstrap toast
    console.log(`[${type}] ${message}`);
}
