var isAuto = true;
var lightOn = true;
var tempOn = true;
var autoOn = true;
var allOn = true;

function setAuto() {
  console.log("auto");
  isAuto = true;
  //Auto button
  document.getElementById("auto").disabled = true;
  document.getElementById("auto").style.backgroundColor = "#111";
  document.getElementById("auto").style.borderColor = "#111";

  //Manual button
  document.getElementById("manual").disabled = false;
  document.getElementById("manual").style.backgroundColor = "#007bff";
  document.getElementById("manual").style.borderColor = "#007bff";

  //Light button
  document.getElementById("light").disabled = true;
  document.getElementById("light").innerHTML = "Accendi Luce";
  document.getElementById("light").style.backgroundColor = "#007bff";
  document.getElementById("light").style.borderColor = "#007bff";

  //Temp button
  document.getElementById("temp").disabled = true;
  document.getElementById("temp").innerHTML = "Accendi Riscaldamento";
  document.getElementById("temp").style.backgroundColor = "#007bff";
  document.getElementById("temp").style.borderColor = "#007bff";

  //All button
  document.getElementById("all").disabled = true;
  document.getElementById("all").innerHTML = "Accendi Entrambi";
  document.getElementById("all").style.backgroundColor = "#007bff";
  document.getElementById("all").style.borderColor = "#007bff";

  sendMessage("buttons#mode#0");
}

function setManual() {
  isAuto = false;
  lightOn = false;
  tempOn = false;
  allOn = false;
  console.log("manuel");

  //Manual Button
  document.getElementById("manual").disabled = true;
  document.getElementById("manual").style.backgroundColor = "#111";
  document.getElementById("manual").style.borderColor = "#111";

  //Auto button
  document.getElementById("auto").disabled = false;
  document.getElementById("auto").style.backgroundColor = "#007bff";
  document.getElementById("auto").style.borderColor = "#007bff";

  //Other button
  document.getElementById("light").disabled = false;
  document.getElementById("temp").disabled = false;
  document.getElementById("all").disabled = false;

  sendMessage("buttons#mode#1");
}

function lightClicked() {
  lightOn = !lightOn;
  console.log("light " + lightOn);

  if (lightOn) {
    document.getElementById("light").style.backgroundColor = "#111";
    document.getElementById("light").style.borderColor = "#111";
    document.getElementById("light").innerHTML = "Spegni Luce";
    sendMessage("buttons#light#1");
  } else {
    document.getElementById("light").style.backgroundColor = "#007bff";
    document.getElementById("light").style.borderColor = "#007bff";
    document.getElementById("light").innerHTML = "Accendi Luce";
    sendMessage("buttons#light#0");
  }
}

function tempClicked() {
  tempOn = !tempOn;
  console.log("temp");

  if (tempOn) {
    document.getElementById("temp").style.backgroundColor = "#111";
    document.getElementById("temp").style.borderColor = "#111";
    document.getElementById("temp").innerHTML = "Spegni Riscaldamento";
    sendMessage("buttons#temp#1");
  } else {
    document.getElementById("temp").style.backgroundColor = "#007bff";
    document.getElementById("temp").style.borderColor = "#007bff";
    document.getElementById("temp").innerHTML = "Accendi Riscaldamento";
    sendMessage("buttons#temp#0");
  }
}

function allClicked() {
  allOn = !allOn;
  console.log("all");

  if (allOn) {
    document.getElementById("all").style.backgroundColor = "#111";
    document.getElementById("all").style.borderColor = "#111";
    document.getElementById("all").innerHTML = "Spegni Entrambi";

    document.getElementById("light").disabled = true;
    document.getElementById("light").style.backgroundColor = "#007bff";
    document.getElementById("light").style.borderColor = "#007bff";
    document.getElementById("light").innerHTML = "Accendi Luce";

    document.getElementById("temp").disabled = true;
    document.getElementById("temp").style.backgroundColor = "#007bff";
    document.getElementById("temp").style.borderColor = "#007bff";
    document.getElementById("temp").innerHTML = "Accendi Riscaldamento";

    sendMessage("buttons#all#1");
  } else {
    document.getElementById("all").style.backgroundColor = "#007bff";
    document.getElementById("all").style.borderColor = "#007bff";
    document.getElementById("all").innerHTML = "Accendi Entrambi";

    document.getElementById("light").disabled = false;
    document.getElementById("temp").disabled = false;
    sendMessage("buttons#all#0");
  }
}
console.log("CIAONE");
setAuto();
loadSettings();
