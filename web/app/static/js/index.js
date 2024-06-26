var isAuto  = true;
var lightOn = true;
var tempOn  = true;
var autoOn  = true;
function setAuto(){
    console.log("auto");
    isAuto = true;
    document.getElementById("light").disabled = true;
    document.getElementById("temp").disabled = true;
    document.getElementById("all").disabled = true;
    document.getElementById("auto").disabled = true;
    document.getElementById("manual").disabled = false;
}
function setManual(){
    isAuto = false;
    console.log("manuel");
    document.getElementById("light").disabled = false;
    document.getElementById("temp").disabled = false;
    document.getElementById("all").disabled = false;
    document.getElementById("auto").disabled = false;
    document.getElementById("manual").disabled = true;
}
//cambai il colore
function lightClicked(){
    lightOn = !lightOn;
    console.log("light " + lightOn);
    document.getElementById("light").value = ((lightOn) ? "Accendi Luce" : "Spegni Luce");
}
function tempClicked(){
    tempOn = !tempOn;
    console.log("temp");
    document.getElementById("temp").disabled = tempOn;
}
function autoClicked(){
    autoOn = !autoOn;
    console.log("auto");
    document.getElementById("all").disabled = autoOn;
    document.getElementById("light").disabled = true;
    document.getElementById("temp").disabled = true;
}
console.log("CIAONE");
setAuto();
// var lastClickedSensor = auto;

//     function updateSensorValues(sensorId, value) {
//       $('#'+sensorId).text(value);
//     }
//     function disableSensors() {
//       var pressureValue1 = $('#pressureValue1').text();
//       var pressureValue2 = $('#pressureValue2').text();

//           if ($('#manual').hasClass('mainBtn') && $('#manual').hasClass('active')) {
//             $('#light').prop('disabled', false);
//             $('#temp').prop('disabled', false);
//             $('#all').prop('disabled', false);
//             $('#auto').removeClass('active');
//           } else {
//             if (pressureValue1 == 'Si' || pressureValue2 == 'Si' || (pressureValue1 == 'Si' && pressureValue2 == 'Si') ) {
//               $('#auto').addClass('active');
//             }
//             $('#light').prop('disabled', true);
//             $('#temp').prop('disabled', true);
//             $('#all').prop('disabled', true);
//         }
      
//     }
        
//     $(document).ready(function() {
//         $('.btn').click(function() {
//             var clickedSensor = $(this).attr('id');
//             if (clickedSensor == 'manual' || clickedSensor == 'auto') {
//                 if (lastClickedSensor == clickedSensor) {
//                     $(this).removeClass('active');
//                     lastClickedSensor = null;
//                 } else {
//                     $('.btn.active').removeClass('active');
//                     $(this).addClass('active');
//                     lastClickedSensor = clickedSensor;
//                 }
//             }
//             else {
//                 $(this).toggleClass('active');
//             }
//             disableSensors();
//         });

//         $('#manual').click(function() {
//             disableSensors();
//         });
        
//         $('#auto').click(function() {
//             disableSensors();
//         });
//     });

