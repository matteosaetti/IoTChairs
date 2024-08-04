/*Add listener to "settings" HTML form for the "submit" event to prevent data sending, reloading
 of the page and the subsequent error -> "webSocket connection to ... failed.."
Then save the settings
*/
document
  .getElementById("settings")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var temperatureThreshold = document.getElementById(
      "temperatureThreshold"
    ).value;
    var lightThreshold = document.getElementById("lightThreshold").value;

    saveSettings(temperatureThreshold, lightThreshold);
  });
//Global variables
var savedLight = 50;
var savedTemperature = 25;

//function for loading save settings
function loadSettings() {
  if (savedTemperature != null) {
    document.getElementById("temperatureThreshold").value = savedTemperature;
  }
  if (savedLight != null) {
    document.getElementById("lightThreshold").value = savedLight;
  }
}

//function for saving new settings
function saveSettings() {
  temperature =
    "settings#settings/temp#" +
    document.getElementById("temperatureThreshold").value;
  light =
    "settings#settings/light#" +
    document.getElementById("lightThreshold").value;
  if (saveAndSendSettings(light, temperature)) {
    Notiflix.Report.success(
      "Successo",
      "Impostazioni salvate con successo!",
      "OK",
      closeNav()
    );
  } else {
    Notiflix.Report.failure(
      "Errore",
      "Impossibile salvare le impostazioni.",
      "ERROR"
    );
  }
}
