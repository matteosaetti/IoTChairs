
console.log("partuto")
const socket = io()

socket.on('message', function(msg) {
    console.log("ecco il messs: "+msg)
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