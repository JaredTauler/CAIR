HeaderTitle("Master")

let None = null
let list = VALUES["list"]

for (let key in list) {
        row = list[key]
        console.log(row)
        let opt = document.createElement('option');

        if (key === "school") {
            opt.text = row["fullname"]
            opt.value = row["id"]
        }

        let select = document.querySelector("#".concat(key));
        select.appendChild(opt);
    }

