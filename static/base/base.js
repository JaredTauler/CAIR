// Cookie om nom nom
{
    // If not logged in, redirect to login screen.
    // This is in case a cached page is being shown, i.e. the user decided to
    // click the back arrow after logging out.
    try {
        let cookie = JSON.parse(document.cookie)
        if (cookie["logged_in"] === false) {
            if (window.location.pathname !== "/login") {
                window.location.replace("login")
            }
        }
    } catch (e) {
        // No redirect if malformed cookie. Just make a new one.
        let cookie = {}
        cookie["logged_in"] = undefined
        document.cookie = JSON.stringify(cookie)
    }
}

// Set the pages title. This expects the header html to be included
function HeaderTitle (s) {
    // Not really critical if this fails.
    try {
        document.getElementById("HeaderTitle").textContent = s
    } catch (e) {console.log("Couldnt set header title!")}
}
