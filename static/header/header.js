// Navigation button thingy.
{
    let NavDropdown = document.getElementById("NavDropdown")
    // On click, show options
    NavDropdown.addEventListener("click", function () {
        NavDropdown.classList.toggle("active")
    })
    // when mouse leaves div, no more showing of options.
    NavDropdown.addEventListener("mouseleave", function () {
        NavDropdown.classList.remove("active")
    })
}

// TODO Logout button
{
    let button = document.getElementById("LogoutButton")
    button.addEventListener("click", function () {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            window.location.replace(window.location)
        }
        };

    xhttp.open("POST", "logout", true);
    xhttp.send();
    })

    //Jquery or vanilla JS???


    //     $.ajax({
    //     type: "POST",
    //     url: window.location.href,
    //     dataType: "json",
    //     processData: false,
    //     contentType: false,
    //     encode: true,
    //     data: formData,
    //
    // // On response data:
    // }).done(function (data) {
    // })
}
