var isPushEnabled = false;

window.addEventListener('load', function() {
    // Your code here
});

// Check that service workers are supported, if so, progressively
// enhance and add push messaging support, otherwise continue without it.
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('static/service-worker.js')
    .then(initialiseState);
} else {
    console.warn('Service workers aren\'t supported in this browser.');
}
