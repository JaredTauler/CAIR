// Prepare elements for use

HeaderTitle("Reports")

// Populate student dropdown
{
    let None = null
    var list = VALUES
    console.log(VALUES)
    for (let key in list) {
        for (let i in list[key]) {
            row = list[key][i]
            console.log(row)
            let opt = document.createElement('option');

            opt.text = "".concat(title(row[1]), " ", title(row[2]));
            opt.value = row[0]
            if (key === "student") {
                document.getElementById("ReportStudentList").appendChild(opt)
            }
            else if (key === "user") {
                document.getElementById("ReportUserList").appendChild(opt)
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
    document.getElementById("Export").style.display = "none"
}

