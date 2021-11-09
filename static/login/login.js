document.getElementById("HeaderTitle").textContent = "Attendance Centralized Interaction Reporting"
document.getElementById("PageTitle").textContent = "Login"

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

$(document).ready(function () {
    $("form").submit(function (event) {
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

        console.log(username.attributes)
        let formData = {
            "username": $("#username").val(),
            "password": $("#password").val(),
        };
        console.log(formData);
        // Post to server
        $.ajax({
            type: "POST",
            url: window.location.href,
            dataType: "json",
            encode: true,
            data: formData,
        // On response data:
        }).done(function (data) {
            if (data[0] === "redirect") {
                window.location.href = data[1]
            }
            // TODO Tell user why couldnt login.
        });

        event.preventDefault();
        return false;
    });
});
