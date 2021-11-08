// TODO cleanup!!!
function title(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function newoption(opt, key) {
    let select = document.querySelector("#".concat(key));
    select.appendChild(opt);
}

// Set date elements default to today's date
// TODO A better way of doing this?
{
    var today = new Date();
    var d = String(today.getDate()).padStart(2, '0');
    var m = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var y = today.getFullYear();
    today = y + '-' + m + '-' + d;
    document.getElementById('date').value = today;
}

// Populate lists #}
{
    let None = null
    var list = VALUES["list"]

    for (let key in list) {
        for (let i in list[key]) {
            row = list[key][i]
            console.log(row)
            let opt = document.createElement('option');

            // Decide how to handle data depending on what list is being drawn from. This seemed like the best
            // way to do it.

            if (key === "studentlist") {
                opt.text = "".concat(title(row["fname"]), " ", title(row["lname"]));
                opt.value = row["id"]
            } else if (key === "action") {
                opt.text = "".concat(row["type"]);
                opt.value = row["id"];
            }

            newoption(opt, key);
        }
    }
}


// Form submission logic.
let form = document.querySelector("#mainform")
$("#mainform").submit(function (event) {
     // Get all data from form.
    let formData = new FormData(document.querySelector('#mainform'))

    // Post to server
    $.ajax({
        type: "POST",
        url: window.location.href,
        dataType: "json",
        processData: false,
        contentType: false,
        encode: true,
        data: formData,

    // On response data:
    }).done(function (data) {
        if (data["result"] === "pick") {
            openModal(PickStudent, data["query"])
        }

        return false
    });

    event.preventDefault();
    return false;
});

