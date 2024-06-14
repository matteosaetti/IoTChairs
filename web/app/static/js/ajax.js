function ajaxCall(){
    var pressure1 = document.getElementById("pressureValue1").value
    var pressure2 = document.getElementById("pressureValue2").value

    var temperature = document.getElementById("temperatureValue").value
    var light = document.getElementById("lightValue").value
    
    $.ajax({
        type: "POST",
        url: "/",
        data: jQuery.param({ 
            pressure1   : pressure1,
            pressure2   : pressure2,
            temperature : temperature,
            light       : light,
        }),
        success: function (response) {
            console.log(response + "TODO ESCI I VALORI")
        },
        error: function (status, error) {
            console.log("AJAX Error, TODO USA NOTIFLIX")
        }
    });
}