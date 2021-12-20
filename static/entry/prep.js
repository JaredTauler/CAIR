HeaderTitle("Interaction Entry")

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
