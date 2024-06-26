
console.log("partuto")
const socket = io()

socket.on('message', function(msg) {
    console.log("ecco il messs: "+msg)
    document.getElementById('temperatureValue').innerHTML = msg + "°C";
});

function sendMessage() {
    console.log("invio")
    socket.send("#LON#on");
}

/*
for(let i=0; i<10; i++){
    console.log("giro "+i)
    sendMessage()
}
*/