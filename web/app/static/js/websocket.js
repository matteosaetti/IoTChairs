console.log("partito");
const socket = io();

//Leggo dal .py
socket.on("sensor/temp", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("temperatureValue").innerHTML = msg + "°C";
});

socket.on("sensor/pressure", function (msg) {
  console.log("ecco il messs: " + msg);
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

socket.on("sensor/light", function (msg) {
  console.log("ecco il messs: " + msg);
  document.getElementById("lightValue").innerHTML = msg + "lux";
});

//Scrivo al .py
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
