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
        } else if (choice === "user") {
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
                            let s = d.toLocaleDateString("en-US")
                            return s
                        },
                    },
                    {
                        title: "Type", field: "type", sorter: "string",
                    }
                ]
            });
        } else if (choice === "student") {
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
                            let s = d.toLocaleDateString("en-US")
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
// Report dropdown
// {
//     let Report = document.getElementById("ReportDropdown")
//     let Date = document.getElementById("DateDropdown")
//     let DateRange = {}
//     // Date.addEventListener("change", function () {
//     //
//     // })
//
//     function SetDate(drop=null, start=null, end=null) {
//         document.getElementById("DateDropdown").hidden = drop
//         document.getElementById("DateStart").hidden = start
//         document.getElementById("DateEnd").hidden = end
//     }
//
//     Report.addEventListener("change", function () {
//         if (Report.value === "name") {
//             SetDate(true, true, true)
//         } else if (Report.value === "student") {
//             SetDate(false, true, true)
//         } else if (Report.value === "user") {
//             SetDate(false, true, true)
//         }
//     })
//
//     Date.addEventListener("change", function () {
//         console.log("1")
//         if (Date.value === "0") {
//             SetDate(false, true, true)
//         } else if (Date.value === "1") {
//             SetDate(false, true, false)
//         } else if (Date.value === "2") {
//             SetDate(false, false, false)
//         }
//     })
//
// }
