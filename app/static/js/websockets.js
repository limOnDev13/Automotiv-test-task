let hour = 00;
let minute = 00;
let second = 00;
var ws = new WebSocket(`ws://localhost:8000/ws`);

ws.onmessage = function(event) {
    var stats = JSON.parse(event.data)

    document.getElementById('CPU').innerHTML = stats.CPU
    document.getElementById('RAM').innerHTML = stats.RAM
    document.getElementById('ROM').innerHTML = stats.ROM
};

function start_timer(event) {
    ws.send("start")
    timer = true;

    hour = 0;
    minute = 0;
    second = 0;

    document.getElementById('hour').innerHTML = "00";
    document.getElementById('min').innerHTML = "00";
    document.getElementById('sec').innerHTML = "00";

    stopWatch();

    document.getElementById("timer").innerHTML = "Остановить";
    document.getElementById("timer").setAttribute("onclick", "end_timer()");
}

function end_timer(event) {
    ws.send("end")
    timer = false;

    document.getElementById("timer").innerHTML = "Начать запись";
    document.getElementById("timer").setAttribute("onclick", "start_timer()");
}

function stopWatch() {
    if (timer) {
        if (second == 60) {
            minute++;
            second = 0;
        }

        if (minute == 60) {
            hour++;
            minute = 0;
            second = 0;
        }

        let hrString = hour;
        let minString = minute;
        let secString = second;

        if (hour < 10) {
            hrString = "0" + hrString;
        }

        if (minute < 10) {
            minString = "0" + minString;
        }

        if (second < 10) {
            secString = "0" + secString;
        }

        document.getElementById('hour').innerHTML = hrString;
        document.getElementById('min').innerHTML = minString;
        document.getElementById('sec').innerHTML = secString;

        setTimeout(stopWatch, 1000);
        second++;
    }
}
