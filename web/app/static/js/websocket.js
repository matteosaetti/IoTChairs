
console.log("partuto")
const socket = io()

socket.on('message', function(msg) {
    console.log("ecco il messs: "+msg)
    document.getElementById('temperatureValue').innerHTML = msg + "°C";
});
socket.on('topico', function(msg) {
    console.log("ecco il messs: "+msg)
    document.getElementById('temperatureValue').innerHTML = msg + "°C";
});
socket.on('sensor/temp', function(msg) {
    console.log("ecco il messs: "+msg)
    document.getElementById('temperatureValue').innerHTML = msg + "°C";
});
socket.on('sensor/pressure', function(msg) {
    console.log("ecco il messs: "+msg)
    const parts = msg.split('.');
    const val   = parts[1];
    if(msg[0] === "1")
    {
        if(val === "1")
            document.getElementById('pressureValue1').innerHTML = "Sì";
        else
            document.getElementById('pressureValue1').innerHTML = "No";
    }
    else
    {
        if(val === "1")
            document.getElementById('pressureValue2').innerHTML = "Sì";  
        else
            document.getElementById('pressureValue2').innerHTML = "No";
    }
});

socket.on('sensor/light', function(msg) {
    console.log("ecco il messs: "+msg)
    document.getElementById('lightValue').innerHTML = msg + "lux";
 
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
