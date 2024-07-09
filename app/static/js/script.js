// Ensure this is included in your HTML files where you need real-time communication
var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log('WebSocket connected!');
});

socket.on('update', function(data) {
    // Handle real-time updates from server
    console.log(data);
});
