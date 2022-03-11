let StudentList = document.getElementById("StudentList")


function StudentSearch() {
    let formData = new FormData(document.getElementById("SearchForm"))
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            response = JSON.parse(xhttp.response)
            if (this.status == 200) {
                ClearStudentList()
                for (let i in response) {
                    console.log(response[i])
                    var option = document.createElement("option");
                    option.text = response[i][0] + " " + response[i][1];
                    option.value = i;
                    StudentList.appendChild(option)
                }
            }
        }
    };
    xhttp.open("POST", "/student_search", true);
    xhttp.send(formData);
    return false
}

function SearchSubmit(id) {
    document.getElementById(id).value = StudentList.value
    HideSearchModal()
}

let SearchModal = document.getElementById("SearchModal");

function ShowSearchModal() {
  SearchModal.style.display = "grid";
}

function HideSearchModal() {
    SearchModal.style.display = "none";
}
function ClearStudentList() {
    while (StudentList.hasChildNodes()) {
        StudentList.removeChild(StudentList.firstChild)
    }
}

ClearStudentList()
