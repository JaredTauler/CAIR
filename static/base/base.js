// Detect if mobile
// TODO good way of doing this?
var isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;

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

function title(str) {
    try {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    } catch (e) {return str} // Ignore error
}

// Set the pages title. This expects the header html to be included
function HeaderTitle (s) {
    // Not really critical if this fails.
    try {
        document.getElementById("HeaderTitle").textContent = s
    } catch (e) {console.log("Couldnt set header title!")}
}

function localedate (str) {
    let d = new Date(str)
    return d.toLocaleDateString('en-US', {timeZone: 'UTC'})
}

// DEBUG
function FormDataPrint (v) {
    for (var pair of v.entries()) {
     console.log(pair[0]+ ': ' + pair[1]);
    }
}
