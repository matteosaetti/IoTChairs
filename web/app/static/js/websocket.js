console.log("Confirmed connection");
const socket = io();

//Function for reading sensor/temp value from .py
socket.on("sensor/temp", function (msg) {
  console.log("message: " + msg);
  document.getElementById("temperatureValue").innerHTML = msg + " °C";
});

//Function for reading sensor/pressure value from .py
socket.on("sensor/pressure", function (msg) {
  console.log("message: " + msg);
  const parts = msg.split("#");
  const val = parts[1];
  if (msg[0] == "1") {
    if (val == "1") document.getElementById("pressureValue1").innerHTML = "Sì";
    else document.getElementById("pressureValue1").innerHTML = "No";
  } else {
    if (val == "1") document.getElementById("pressureValue2").innerHTML = "Sì";
    else document.getElementById("pressureValue2").innerHTML = "No";
  }
});

//Function for reading sensor/light value from .py
socket.on("sensor/light", function (msg) {
  console.log("message: " + msg);
  document.getElementById("lightValue").innerHTML = msg + " lux";
});

//Function for writing buttons values from .py
function sendMessage(msg) {
  console.log(msg);
  var msgSplit = msg.split("#");
  if (msgSplit.length < 3) return;
  var from = msgSplit[0];
  var topic = msgSplit[1];
  var value = msgSplit[2];
  console.log(msgSplit);
  socket.emit(from, topic + "#" + value);
}

//Function for writing settings values from .py
function saveAndSendSettings(lightThreshold, tempThreshold) {
  console.log(
    "New Thresholds are setted: Light: " +
      lightThreshold +
      " Temperature: " +
      tempThreshold
  );
  var lightSplit = lightThreshold.split("#");
  var fromLight = lightSplit[0];
  var topicLight = lightSplit[1];
  var valueLight = lightSplit[2];

  var tempSplit = tempThreshold.split("#");
  var fromTemp = tempSplit[0];
  var topicTemp = tempSplit[1];
  var valueTemp = tempSplit[2];

  console.log(tempSplit);
  console.log(lightSplit);
  socket.emit(fromLight, topicLight + "#" + valueLight);
  socket.emit(fromTemp, topicTemp + "#" + valueTemp);
  return true;
}
