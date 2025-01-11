var ws = new WebSocket(`ws://localhost:8000/ws`);
ws.onmessage = function(event) {
    var stats = JSON.parse(event.data)

    document.getElementById('CPU').innerHTML = stats.CPU
    document.getElementById('RAM').innerHTML = stats.RAM
    document.getElementById('ROM').innerHTML = stats.ROM
};
