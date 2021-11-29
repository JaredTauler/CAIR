HeaderTitle("Master")

let None = null
let list = VALUES["list"]

for (let key in list) {
    for (let i in list[key]) {
        row = list[key][i]
        console.log(row)
        let opt = document.createElement('option');

        if (key === "school") {
            opt.text = row["fullname"]
            opt.value = row["id"]
        }

        let select = document.querySelector("#".concat(key));
        select.appendChild(opt);
    }
}
