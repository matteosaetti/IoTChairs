//TODO DA REFACTORARE
function loadSettings() {
  
  var savedTemperature = localStorage.getItem('temperatureThreshold');
    var savedLight = localStorage.getItem('lightThreshold');

    if (savedTemperature !== null) {
        $('#temperatureThreshold').val(savedTemperature);
        $('#savedTemperature').text(savedTemperature);
    }
    if (savedLight !== null) {
        $('#lightThreshold').val(savedLight);
        $('#savedLight').text(savedLight);
    }
}

function saveSettings(temperature, light) {
  localStorage.setItem('temperatureThreshold', temperature);
  localStorage.setItem('lightThreshold', light);

  if (localStorage.getItem('temperatureThreshold') === temperature &&
      localStorage.getItem('lightThreshold') === light) {
    $('#savedTemperature').text(temperature);
    $('#savedLight').text(light);
    Notiflix.Report.success('Successo', 'Impostazioni salvate con successo!', 'OK', closeNav());
  } else {
    Notiflix.Report.failure('Errore', 'Impossibile salvare le impostazioni.', 'ERROR');
  }
}

$('#settingsForm').submit(function(event) {
    event.preventDefault();

    var temperatureThreshold = $('#temperatureThreshold').val();
    var lightThreshold = $('#lightThreshold').val();

    saveSettings(temperatureThreshold, lightThreshold);

});