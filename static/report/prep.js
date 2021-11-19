// Prepare elements for use

HeaderTitle("Reports")

// Populate Lists
function title(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Populate student dropdown
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
                document.getElementById("ReportStudentList").appendChild(opt)
            }
        }
    }
}

// Set date element's date.
{
    {
        Date.prototype.addDays = function(days) {
            var date = new Date(this.valueOf());
            date.setDate(date.getDate() + days);
            return date;
        }

        function DatePlaceholder (date) {
            var d = String(date.getDate()).padStart(2, '0');
            var m = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
            var y = date.getFullYear();
            date = y + '-' + m + '-' + d;
            return date;
        }

        let today = new Date();
        document.getElementById('DateStart').value = DatePlaceholder(today);
        document.getElementById('DateEnd').value = DatePlaceholder(today.addDays(1));

    }
}


if (isMobile) {console
    console.log("BRUUHHHHHHH")
    document.getElementById("Export").style.display = "none"
}

