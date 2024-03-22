// my/userdetails.js


document.addEventListener("DOMContentLoaded", function () {
    renderMyUserDetails();
});


// render my user details
async function renderMyUserDetails() {
    const userDetails = await fetchMyUserDetails();
    const userDetailsList = document.getElementById("user-details");

    // clear the previous user details list
    userDetailsList.textContent = "";

    const listItem = `
        <li>お名前</li>
        <li>${userDetails.last_name}　${userDetails.first_name}</li>
        <li>ふりがな</li>
        <li>${userDetails.last_name_furigana}　${userDetails.first_name_furigana}</li>
        <li>電話番号</li>
        <li>${userDetails.tel}</li>
        <li>〒郵便番号</li>
        <li>${userDetails.postal_code}</li>
        <li>住所</li>
        <li>${userDetails.address}</li>
        <li>ユーザー名</li>
        <li>${userDetails.username}</li>
    `;

    if (userDetails.length == 0) {
        userDetailsList.textContent = "<p>情報を取得できませんでした</p>";
    };

    userDetailsList.insertAdjacentHTML("beforeend", listItem);
};



// get my user details
async function fetchMyUserDetails() {
    const token = loadAccessToken();
    const response = await fetch("/json/my/userdetails", {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
    });
    if (response.ok) {
        const userDetails = await response.json();
        console.log("success: fetchMyUserDetails()", userDetails);
        return userDetails;
    } else {
        console.error("error: fetchMyUserDetails()");
        return [];
    };
};

