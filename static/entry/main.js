function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

function newoption(opt, key) {
    let select = document.querySelector("#".concat(key));
    select.appendChild(opt);
}

// event listener for when user changes it
document.getElementById("student_id").addEventListener("focusout", function () {
    CheckID()
})
// Check if data is OK. There should be another check on the server too.
function CheckID () {
    let id = document.getElementById("student_id")
    if (!isNumeric(id.value)) {
        id.classList.add("badbox")
        return false
    } else {
        id.classList.remove("badbox")
        return true
    }
}

// Form submission logic.
// let form = document.querySelector("#mainform")
// $("#mainform").submit(function (event) {
//     if (!CheckID()) {return false} // If no ID, dont bother sending POST.
//
//     // Get all data from form.
//     let formData = new FormData(document.querySelector('#mainform'))
//
//     // Post to server
//     $.ajax({
//         type: "POST",
//         url: window.location.href,
//         dataType: "json",
//         processData: false,
//         contentType: false,
//         encode: true,
//         data: formData,
//
//     // On response data:
//     }).done(function (data) {
//
//     });
//
//     event.preventDefault();
//     return false;
// });
document.getElementById("submitbutton").addEventListener("click", function() {
    let formData = new FormData(document.getElementById("mainform")) // Get form data
    if (!CheckID()) {return false} // If no ID, dont bother sending POST.

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        console.log(this.status)
        if (this.readyState == 4) { // If ready
            if (this.response !== "") {
                response = JSON.parse(this.response)
            }
            if (this.status == 200) {
                // if (data["result"] === "pick") {
                //     openModal(PickStudent, data["query"])
                // }

                return false
            }
        }
    };

    xhttp.open("POST", window.location.href, false);
    xhttp.send(formData);

    return false;
})
