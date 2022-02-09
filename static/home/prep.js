HeaderTitle("Home")

let elem = {
    "report": "Reports Statistics",
    "entry": "Ticket Entry",
    "student_master": "Student Master",
    "worker_master": "Worker Master",
}

for (let i in elem) {
    console.log(elem[i])
    let newobj = document.createElement("input")
    newobj.setAttribute("class", "smooth, glowfocus, button")
    newobj.setAttribute("type", "button")
    newobj.setAttribute("value", elem[i])
    newobj.addEventListener("click", function () {
        window.location.href = '/'.concat(i)
    })
    document.getElementById("wrapper").appendChild(newobj)
}

