HeaderTitle("Interaction Entry")

// Set date elements default to today's date
document.getElementById('date').value = getDate()

// Populate lists #}
{
    let None = null
    var list = VALUES["list"]
    console.log(list)
    for (let key in list) {
        for (let i in list[key]) {
            row = list[key][i]
            console.log(row, i)
            let opt = document.createElement('option');

            if (key === "studentlist") {
                opt.text = "".concat(title(row[1]), " ", title(row[2]));
                opt.value = row[0];
            } else if (key === "action") {
                opt.text = row[0];
                opt.value = i;
            }
            newoption(opt, key);
        }
    }
}
