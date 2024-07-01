console.log("partito");
const socket = io();

//Leggo dal .py
socket.on("message", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("temperatureValue").innerHTML = msg + "°C";
});

socket.on("topico", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("temperatureValue").innerHTML = msg + "°C";
});

socket.on("sensor/temp", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("temperatureValue").innerHTML = msg + "°C";
});

socket.on("sensor/pressure", function (msg) {
  console.log("ecco il messs: " + msg);
  const parts = msg.split(".");
  const val = parts[1];
  if (msg[0] == "1") {
    if (val == "1") document.getElementById("pressureValue1").innerHTML = "Sì";
    else document.getElementById("pressureValue1").innerHTML = "No";
  } else {
    if (val == "1") document.getElementById("pressureValue2").innerHTML = "Sì";
    else document.getElementById("pressureValue2").innerHTML = "No";
  }
});

socket.on("sensor/light", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("lightValue").innerHTML = msg + "lux";
});

//Scrivo al .py
function sendMessage(msg) {
  console.log(msg);
  var msgTrim = msg.split("#");
  var from = msgTrim[0];
  var value = msgTrim[1];
  console.log("message from " + from + "= " + value);
  socket.emit(from, value);
}

function saveAndSendSettings(lightThreshold, tempThreshold) {
  console.log(
    "New Thresholds are setted: Light: " +
      lightThreshold +
      " Temperature: " +
      tempThreshold
  );
  var lightTrim = lightThreshold.split("#");
  var fromLight = lightTrim[0];
  var valueLight = lightTrim[1];

  var tempTrim = tempThreshold.split("#");
  var fromTemp = tempTrim[0];
  var valueTemp = tempTrim[1];

  socket.emit(fromLight, valueLight);
  socket.emit(fromTemp, valueTemp);
  return true;
}
