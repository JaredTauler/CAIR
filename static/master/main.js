let ReportTable = document.getElementById("ReportTable");
let ReportTableTabulator = new Tabulator("#ReportTable", );

// On fetch button click,
document.getElementById("ReportFetch").addEventListener("click", function(){
    let formData = new FormData(document.getElementById("ReportForm")) // Get form data
    formData.append('isMobile', isMobile); // add mobile tag to formdata.

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(xhttp.response)

            // Table
            {
                ReportTable.hidden = false
                document.getElementById("ReportTable").hidden = false
                ReportTableTabulator = TableFormat(response["table"])
            }

            let man = response["man"][0] // auto indexed
            ChangeForm.disable(false)
            ChangeForm["fname"].value = man[0]
            ChangeForm["lname"].value = man[1]
            ChangeForm["school"].selected = man[2]
            console.log(ChangeForm["school"].value) //FIXME continue

        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

    return false;
})
