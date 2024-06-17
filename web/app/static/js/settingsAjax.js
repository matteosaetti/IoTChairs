function settingsAjaxCall(){
    var temperatureThreshold = document.getElementById("temperatureThreshold").value
    var lightThreshold = document.getElementById("lightThreshold").value
    
    $.ajax({
        type: "POST",
        url: "/settings",
        data: jQuery.param({ 
            temperatureThreshold : temperatureThreshold,
            lightThreshold       : lightThreshold,
        }),
        success: function (response) {
            console.log(response + "TODO ESCI I VALORI")
        },
        error: function (status, error) {
            console.log("AJAX Error, TODO USA NOTIFLIX")
        }
    });
}