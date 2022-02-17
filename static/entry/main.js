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
                PopupText("Success")
                ShowPopup()
                return false
            }
        }
    };

    xhttp.open("POST", window.location.href, false);
    xhttp.send(formData);

    return false;
})
