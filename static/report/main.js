ReportTable = document.getElementById("ReportTable")
ReportTableTabulator = new Tabulator("#ReportTable", {
    autoColumns:true,
});

// On fetch button click,
document.getElementById("ReportFetch").addEventListener("click", function(){
    let formData = new FormData(document.getElementById("ReportForm")) // Get form data
    formData.append('isMobile', isMobile); // add mobile tag to formdata.

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) { // If ready
            response = JSON.parse(xhttp.response)
            if (this.status == 200) {
                ReportTable.hidden = false
                document.getElementById("ReportTable").hidden = false
                if (response["table"]) {
                    ReportTableTabulator = TableFormat(
                        document.getElementById("ReportDropdown").value,
                        response["table"]
                    )
                } else {
                    console.log("no data")
                    // TODO no data
                }
            }
        }
    };

    xhttp.open("POST", window.location.href, true);
    xhttp.send(formData);

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
    // Run once after done setting up listeners.
    DropDownDecide()
}

// This relies on the table format including hidden tables!
function ExcelExport () {
    ReportTableTabulator.download("csv", "data.csv", {sheetName:"MyData"});
}
