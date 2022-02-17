var modal = document.getElementById("myModal");

function ShowPopup() {
  modal.style.display = "grid";
}
function PopupText(str) {
  document.getElementById("modal-text").textContent = str
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function PopupError(response) {
  console.log(response)
    PopupText("An error occurred on the server: "  + response["error"])
}
