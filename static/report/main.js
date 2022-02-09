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
// Im sure there is a much more simpler way of doing this. I dont know that way, but this works flawlessly.
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
    var EntryDrop = document.getElementById("EntryDrop")
    let text = document.getElementById("EntryBox")

    DropDown.addEventListener("change", function() {DropDownDecide()})

    function DropDownDecide () {
        function EntryText (s) {
            text.placeholder = s
            text.hidden = false
            EntryDrop.hidden = true
        }
        function SetEntryDrop (s) {
            while (EntryDrop.hasChildNodes()) {
                EntryDrop.firstChild.remove()
            }

            for (let key in s) {
                console.log(key)
                let opt = document.createElement('option');
                opt.value = key;
                opt.text = s[key];
                EntryDrop.appendChild(opt);
            }
            text.hidden = true
            EntryDrop.hidden = false
        }
        function DropDecide(valueToSelect) {
            EntryDrop.value = valueToSelect;
        }

        let state = false

        if (DropDown.value === "name") {
            state = [0,0,0,0,0]
            EntryText("")
        }
        else if (DropDown.value === "student") {
            state = [1,1,1,1,1]
            EntryText("Student ID")
        }
        else if (DropDown.value === "user") {
            state = [1,1,1,1,1]
            EntryText("User ID")
        }
        else if (DropDown.value === "school_percent") {
            state = [1,1,1,1,1]
            EntryText("")
            SetEntryDrop(
                Object.assign({},
                    VALUES["man"]["school"],
                    {"all": "All Schools"}
                )
            )
            DropDecide("all")
        }
        else if (DropDown.value === "action_type") {
            state = [1,1,1,1,1]
            SetEntryDrop(
                // Options for dropdown is action table query + everything
                Object.assign(
                    {},
                    VALUES["drop"]["action_type"],
                    {"all": "Everything"}

                )
            )
            DropDecide("all")
        }
        else if (DropDown.value === "action_average") {
           state = [1,1,1,1,0]
            EntryText("")
        }
        else {
            state = [0,0,0,0,0]
            EntryText("")
        }


        // List of elements to be updated
        let ElemList = [
            "DateStart", "DateEnd",
            "DateStartCheckbox", "DateEndCheckbox",
            "EntryBox"
        ]
        let ElemArray = {}
        for (let i in state) {
            ElemArray[ElemList[i]] = state[i] === 0
        }

        // run the Checkbox logic with the previously made array to see if any elements need to be left disabled.
        if (ElemArray["DateStart"] === false) {
            ElemArray = CheckBoxDecide(ElemArray)
        }

        DateState(ElemArray)
    }
    // Run once after done setting up.
    DropDownDecide()
}

// This relies on the table format including hidden tables!
function ExcelExport () {
    ReportTableTabulator.download("xlsx", "data.xlsx", {sheetName:"MyData"});
}
