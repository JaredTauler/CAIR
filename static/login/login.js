HeaderTitle("Attendance Centralized Interaction Reporting")
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

document.getElementById("LoginButton").addEventListener("click", function(){
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

    let formData = {
        "username": $("#username").val(),
        "password": $("#password").val(),
    };

    $.ajax({
        type: "POST",
        url: window.location.href,
        dataType: "json",
        encode: true,
        data: formData,
    // On response data:
    }).done(function (data) {
        if (data[0] === "bad") {
            PopupText("Wrong " + data[1] + ".")
            ShowPopup()
        }
        if (data[0] === "redirect") {
            let cookie = JSON.parse(document.cookie)
            cookie["logged_in"] = true
            document.cookie = JSON.stringify(cookie)
            window.location.href = data[1]


        }

    });

    event.preventDefault();
    return false;
});
