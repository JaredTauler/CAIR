

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
            ReportTable.hidden = false
            document.getElementById("ReportTable").hidden = false
            ReportTableTabulator = TableFormat(response["tabul"])
        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

    return false;
})
