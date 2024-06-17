function ajaxCall(){
    var pressureValue1 = document.getElementById("pressureValue1").value
    var pressureValue2 = document.getElementById("pressureValue2").value

    var temperature = document.getElementById("temperatureValue").value
    var light = document.getElementById("lightValue").value
    
    $.ajax({
        type: "POST",
        url: "/",
        data: jQuery.param({ 
            pressureValue1   : pressureValue1,
            pressureValue2   : pressureValue2,
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