// base.js

// sign up form
document.getElementById("sign-up-form").addEventListener("submit", function(event) {
    event.preventDefault(); // prevent the default form sending

    // get the form data and define the sending data
    const formData = new FormData(document.getElementById("sign-up-form"));
    
    const sendingData = {
        username: formData.get("username"),
        plain_password: formData.get("password")
    };
    
    // send a post request to the endpoint
    fetch("/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(sendingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        location.reload();
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});

