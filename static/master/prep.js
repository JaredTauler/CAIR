HeaderTitle("Master")

// Form that manipulates student data.
const ChangeForm = {}
{
    let x = ["fname", "lname", "school", "active", "last"]

    let a = document.getElementById("changeform")

    for (let i in x) {
        let y = x[i]
        ChangeForm[y] = a.querySelector("#".concat(y))

        // My first JS method. (hehe)
        // Disables all the elements.
        ChangeForm.disable = function (bool) {
            for (let i in ChangeForm) {
                ChangeForm[i].disabled = bool
            }
        }
    }
}
ChangeForm.disabled = true // in case cached page

// setup school dropdown.
{
    let list = VALUES["list"]
    let dropdown = ChangeForm["school"]
    for (let key in list) {
        for (let i in list[key]) {
            row = list[key][i];
            let opt = document.createElement('option');

            if (key === "school") {
                opt.text = row["fullname"];
                opt.value = row["id"];
            }

            dropdown.appendChild(opt);
        }
    }
}

