HeaderTitle("Reports")

// Populate Lists
function title(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
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

var ReportTable = document.getElementById("ReportTable")
var ReportTableTabulator = new Tabulator("#ReportTable", {
    autoColumns:true, //create columns from data field names
});

// On fetch button click,
document.getElementById("ReportFetch").addEventListener("click", function(){
    let formData = new FormData(document.getElementById("ReportForm")) // Get form data
    for (var pair of formData.entries()) {
         console.log(pair[0]+ ': ' + pair[1]);
    }
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
        console.log(data)
        ReportTable.hidden = false
        document.getElementById("ReportTable").hidden = false
        let choice = document.getElementById("ReportDropdown").value
        if (choice === "name") {
            console.log(data)
            const ReportTableTabulator = new Tabulator("#ReportTable", {
                data: data,
                columns: [
                    {
                        title: "Student", field: "name", sorter: "string", width: 200,
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            return title(row["fname"]) + " " + title(row["lname"]);
                        },
                    },
                    {
                        title: "Home School", field: "shortname", sorter: "string",
                    }
                ]
            });
        }
        else if (choice === "user") {
             const ReportTableTabulator = new Tabulator("#ReportTable", {
                data: data,
                columns: [
                    {
                        title: "User", field: "user", sorter: "string", width: 200,
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            return title(row["user_fname"]) + " " + title(row["user_lname"]);
                        },
                    },
                    {
                        title: "Student", field: "student", sorter: "string",
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            return title(row["student_fname"]) + " " + title(row["student_lname"]);
                        },
                    },
                    //
                    {
                        title: "Date", field: "date", sorter: "string",
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            let d = new Date(row["date"])
                            let s = d.toLocaleDateString('en-US', {timeZone: 'UTC'})
                            return s
                        },
                    },
                    {
                        title: "Type", field: "type", sorter: "string",
                    }
                ]
            });
        }
        else if (choice === "student") {
            const ReportTableTabulator = new Tabulator("#ReportTable", {
                data: data,
                columns: [
                    {
                        title: "Student ", field: "student", sorter: "string", width: 200,
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            return title(row["fname"]) + " " + title(row["lname"]);
                        },
                    },
                    {
                        title: "Date", field: "date", sorter: "string",
                        formatter: function (cell) {
                            let row = cell.getRow().getData();
                            let d = new Date(row["date"])
                            let s = d.toLocaleDateString('en-US', {timeZone: 'UTC'})
                            return s
                        },
                    },
                                                {
                        title: "Type", field: "type", sorter: "string",
                    },
                ]
            });
        }
    })


    // event.preventDefault();
    return false;
})

// Logic for when date elements should be disabled or enabled.
// Im sure there is a much more simpler way of doing this. I dont know that way, but this works flawlessly and efficently.
{
    let StartCheckBox = document.getElementById("DateStartCheckbox")
    StartCheckBox.addEventListener("change", function () {
        DateState(CheckBoxDecide({}))
    })
    let EndCheckBox = document.getElementById("DateEndCheckbox")
    EndCheckBox.addEventListener("change", function () {
        DateState(CheckBoxDecide({}))
    })

    function CheckBoxDecide(arr) {
        // If one checkbox is changed, both check boxes will have their associated
        // elements updated according to their current state.
        // This is unncecessary but probably wont cause any problems.
        // FIXME?
        if(StartCheckBox.checked) {
            arr["DateStart"] = false
            arr["DateEndCheckbox"] = false
        }
        else {
            arr["DateStart"] = true
            arr["DateEndCheckbox"] = true
            EndCheckBox.checked = false
        }

        if(EndCheckBox.checked) {arr["DateEnd"] = false}
        else {arr["DateEnd"] = true}

        return arr
    }

    function DateState (arr) {
        for (let i in arr) {
            document.getElementById(i).disabled = arr[i]
        }
    }

    let DropDown = document.getElementById("ReportDropdown")

    DropDown.addEventListener("change", function() {DropDownDecide()})
    function DropDownDecide () {
         // May as well do entrybox placeholder while were here.
        function EntryText (s) {
            document.getElementById("EntryBox").placeholder = s
        }

        let state = false

        if (DropDown.value === "name") {
            state = true
            EntryText("")
        }
        else if (DropDown.value === "student") {
            state = false
            EntryText("Student ID")
        }
        else if (DropDown.value === "user") {
            state = false
            EntryText("User ID")
        }
        else {
            state = true
            EntryText("")
        }

        // List of elements to be updated
        let ElemArray = {
            "DateStart": state, "DateEnd": state,
            "DateStartCheckbox": state, "DateEndCheckbox": state,
            "EntryBox": state

        }

        // If the disabled property is being set to false, run the Checkbox logic with the previously made array to see
        // if any elements need to be left disabled.
        if (state === false) {
            ElemArray = CheckBoxDecide(ElemArray)
        }

        DateState(ElemArray)
    }

    DropDownDecide() // Run when page starts
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
