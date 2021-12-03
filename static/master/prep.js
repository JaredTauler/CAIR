HeaderTitle("Master")

let ReportTable = document.getElementById("ReportTable");
let ReportTableTabulator = new Tabulator("#ReportTable", );
let TableDiv = document.getElementById("tablediv")
let EntryBox = document.getElementById("EntryBox")

// Form that manipulates student data.
const ChangeForm = {}
{
    let x = ["fname", "lname", "school", "active", "last", "id"]

    let a = document.getElementById("changeform")

    for (let i in x) {
        let y = x[i]
        ChangeForm[y] = a.querySelector("#".concat(y))

        ChangeForm.disabled = true
        // My first JS method. (hehe)
        // Disables all the elements.
        ChangeForm.disable = function (bool) {
            if (this.disabled === true) {
                for (let i in ChangeForm) {
                    ChangeForm[i].disabled = bool
                    ChangeForm[i].value = null
                }
            }
        }
    }
}
// document.getElementById("last").hidden = true
const Statistic = {}
Statistic["last"] = document.getElementById("lastval")
Statistic["total"] = document.getElementById("totalval")
Statistic.hidden = function (bool) {
    let x = []
    x["total"] = document.getElementById("total")
    x["last"] = document.getElementById("last")

    for (let i in x) {
        x[i].hidden = bool
    }
}


// setup school dropdown.
{
    let None = null
    let list = VALUES

    for (let key in list) {
        for (let i in list[key]) {
            row = list[key][i]

            // var option = document.createElement("option");
            // option.text = "Text";
            // option.value = "myvalue";
            // var select = document.getElementById("id-to-my-select-box");
            // select.appendChild(option);
            let opt = document.createElement('option');

            if (key === "student") {
                opt.text = "".concat(title(row[1]), " ", title(row[2]));
                opt.value = row[0]
                document.getElementById("ReportStudentList").appendChild(opt)
            }
            else if (key === "school") {

                opt.value = row[0];
                opt.text = row[1];
                ChangeForm["school"].appendChild(opt);
            }
        }
    }
}
function Clear() {
    console.log("Clearing")
    Statistic.hidden(true)
    EntryBox.textContent = null
    ChangeForm.disable(true)
    TableDiv.hidden = true
}
Clear()
