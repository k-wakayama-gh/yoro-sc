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
        <li>メールアドレス</li>
        <li>${userDetails.email}</li>
        <li>ユーザー名</li>
        <li>${userDetails.username}</li>
    `;

    if (userDetails.length == 0) {
        userDetailsList.textContent = "<p>情報を取得できませんでした</p>";
    };

    userDetailsList.insertAdjacentHTML("beforeend", listItem);
    displayEditForm(userDetails);
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




function displayEditForm (userDetails) {
    const listItem = `
        <div class="form-text">お名前<span class="form-annotation">必須</span></div>
        <div class="flex-row-between">
            <input type="text" name="last_name" placeholder="姓" required class="half-input" value="${userDetails.last_name}">
            <input type="text" name="first_name" placeholder="名" required class="half-input" value="${userDetails.first_name}">
        </div>
        <div class="space"></div>
        <div class="form-text">ふりがな<span class="form-annotation">必須</span></div>
        <div class="flex-row-between">
            <input type="text" inputmode="kana-name" name="last_name_furigana" placeholder="ふりがな (姓)" required class="half-input" value="${userDetails.last_name_furigana}">
            <input type="text" inputmode="kana-name" name="first_name_furigana" placeholder="ふりがな (名)" required class="half-input" value="${userDetails.last_name_furigana}">
        </div>
        <div class="space"></div>
        <div class="form-text">電話番号<span class="form-annotation">必須</span></div>
        <input type="tel" name="tel" placeholder="電話番号 (できれば携帯電話)" required value="${userDetails.tel}">
        <div class="space"></div>
        <div class="form-text">郵便番号<span class="form-annotation">必須</span></div>
        <input type="tel" name="postal_code" placeholder="郵便番号" required value="${userDetails.postal_code}">
        <div class="space"></div>
        <div class="form-text">住所<span class="form-annotation">必須</span></div>
        <input type="text" name="address" placeholder="住所" required value="${userDetails.address}">
        <div class="space"></div>
        <div class="form-text">メールアドレス<span class="form-annotation-1">任意</span></div>
        <input type="email" name="email" placeholder="メールアドレス" oninput="autoInputUsername(this)" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$" value="${userDetails.email}">
        <div class="form-text" style="font-size: small; color: gray;">-> 申し込みの確認メールを受け取れます</div>
        <div class="space"></div>
        <div class="form-text">ユーザー名<span class="form-annotation">必須</span></div>
        <input type="text" inputmode="latin" name="username" id="username-input" placeholder="ユーザー名" pattern=".{4,}" required value="${userDetails.username}">
        <div class="form-text" style="font-size: small; color: gray;">-> 本人確認に使用します　半角英数字4文字以上</div>
        <div class="space"></div>
        <div class="form-text">パスワード<span class="form-annotation">必須</span></div>
        <input type="password" inputmode="latin" name="password" placeholder="パスワード" pattern="^([a-zA-Z0-9]{4,})$" required>
        <div class="form-text" style="font-size: small; color: gray;">-> 本人確認に使用します　半角英数字4文字以上</div>
        <div class="space"></div>
        <button type="button" id="edit-check-btn">変更する</button>
        <div class="space"></div>
        <button type="button" id="edit-cancel-btn">変更しない</button>
    `;
    document.getElementById("user-details-edit-form").insertAdjacentHTML("beforeend", listItem);
};



// document.getElementById("edit-btn").addEventListener("click", function () {
//     document.getElementById("user-detail-edit-section").classList.remove("hidden");
//     document.getElementById("user-detail-section").classList.add("hidden");
// });



document.getElementById("edit-cancel-btn").addEventListener("click", function () {
    document.getElementById("user-detail-edit-section").classList.add("hidden");
    document.getElementById("user-detail-section").classList.remove("hidden");
});


