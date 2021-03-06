
// On fetch button click,
// document.getElementById("FetchForm").addEventListener("submit", Fetch)

function Fetch(){
    NewID = false
    let formData = new FormData(document.getElementById("FetchForm")) // Get form data
    formData.append('isMobile', isMobile); // add mobile tag to formdata.
    formData.append("intent", "query")
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            response = JSON.parse(xhttp.response)
            if (this.status == 400) {
                PopupText(response["comment"])
                ShowPopup()
            }
            if (this.status == 200) {

                // Table
                if (response["table"] !== undefined) {
                    let RowCount = Object.keys(response["table"]["main"]).length
                    Statistic.hidden(false)
                    Statistic["total"].textContent = RowCount
                    document.getElementById("ReportTable").hidden = false
                    ReportTableTabulator = TableFormat(response["table"])
                    TableDiv.hidden = false

                    // Find Latest date.
                    let bigger = "0"
                    let x = "0"

                    function num(x) {
                        x = x.replace(new RegExp("-", 'g'), "")
                        return Number(x)
                    }

                    for (let value of Object.values(response["table"]["main"])) {
                        x = value[0]
                        if (num(x) > num(bigger)) {
                            bigger = x
                        }
                    }

                    Statistic["last"].textContent = localedate(bigger)
                } else {
                    console.log("no tickets")
                    // todo no data
                }

                let man = response["man"][0] // auto indexed
                ChangeForm.disable(false)
                ChangeForm["id"].value = man[0]
                ChangeForm["fname"].value = man[1]
                ChangeForm["lname"].value = man[2]
                ChangeForm["school"].value = man[3]
                ChangeForm["active"].checked = man[4] // data already fits, (1 = checked, 0 = not)

            }
        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

    return false;
}

function Save () {
    let formData = new FormData(document.getElementById("changeform")) // Get form data
    formData.append('isMobile', isMobile); // add mobile tag to formdata.
    if (NewID) formData.append("intent", "new")
    else formData.append("intent", "save")
    formData.append("EntryBox", document.getElementById("EntryBox").value)
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                PopupText("Succesfully saved")
                ShowPopup()
            }
            else if (this.status == 500) {
                response = JSON.parse(xhttp.response)
                PopupError(response)
                ShowPopup()
            }
        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

    return false;
}

EntryBox.addEventListener("click", Clear)

document.getElementById("buttonnew").addEventListener("click", function()
    {
        NewID = true
        ChangeForm.disable(false)
    }
)
