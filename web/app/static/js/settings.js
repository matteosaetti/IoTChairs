/*aggiungo listener e prevengo l'invio dei dati e il reload
prevenire l'evento "submit", il reload della pagina
e il successivo errore -> webSocket connection to .. failed 
aggiungendo un listener e preventDefault
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
var savedLight = 300;
var savedTemperature = 25;
function loadSettings() {
  if (savedTemperature != null) {
    document.getElementById("temperatureThreshold").value = savedTemperature;
  }
  if (savedLight != null) {
    document.getElementById("lightThreshold").value = savedLight;
  }
}

function saveSettings() {
  temperature =
    "settings#tempSet=" + document.getElementById("temperatureThreshold").value;
  light =
    "settings#lightSet=" + document.getElementById("lightThreshold").value;
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
