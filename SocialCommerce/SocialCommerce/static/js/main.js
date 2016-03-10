/**
 * Created by Justin on 3/1/2016.
 */

$(document).ready(function () {
    $("#loginBtn").click(function () {
        Submit();
    });

    $("#reset").click(function () {
        window.location = window.location.href
    });

});

if (document.layers) {
    document.captureEvents(Event.KEYDOWN);
}

document.onkeydown = function (evt) {
    var keyCode = evt ? (evt.which ? evt.which : evt.keyCode) : event.keyCode;
    if (keyCode == 13) {
        Submit();
    }
};

function Submit() {
    $("#submit").click();
}

onload = function () {
    var e = document.getElementById("refreshed");
    if (e.value == "no")e.value = "yes";
    else {
        e.value = "no";
        location.reload();
    }
}