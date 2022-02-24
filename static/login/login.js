HeaderTitle("Centralized Attendance Interaction Reporting")
let username = document.querySelector("#username")
let password = document.querySelector("#password")
const FormElements = [username, password]
// Create a function that runs the check element function?... this is intentional, as
// just passing CheckElement() would give the RESULT of CheckElement() as the listener's function.
username.addEventListener("change", function(){CheckElement(username)});
password.addEventListener("change", function(){CheckElement(password)});

// TODO add more checks on the username and password.
function CheckElement(element) {
    let text = element.value
        console.log(text)
        if (text === "") {
            return true
        };
    return false
};

function login() {
    let exit = false
    // Check each element before going ahead with the POST.
    FormElements.forEach(function (x, i)
        {if (CheckElement(x)) {
                exit = true
                return false // Break loop
            }
        }
    )
    if (exit) {return false} // Break function if loop found elements guilty.

    let formData = new FormData(document.getElementById("LoginForm"))
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            response = JSON.parse(xhttp.response)
            if (this.status == 200) {
                if (response[0] === "bad") {
                    PopupText("Wrong " + response[1] + ".")
                    ShowPopup()
                }
                if (response[0] === "redirect") {
                    let cookie = JSON.parse(document.cookie)
                    cookie["logged_in"] = true
                    document.cookie = JSON.stringify(cookie)
                    window.location.href = response[1]


                }
            }
            else if (this.status == 500) {
                PopupError(response)
                ShowPopup()
            }
        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

    return false;
};
