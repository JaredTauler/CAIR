// Cookie om nom nom
{
    let cookie = JSON.parse(document.cookie)
    // If not logged in, redirect to login screen.
    // This is in case a cached page is being shown, i.e. the user decided to
    // click the back arrow after logging out.
    try {
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

