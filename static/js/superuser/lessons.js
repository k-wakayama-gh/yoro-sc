// superuser/lessons.js

// create: add lesson from
document.getElementById("add-lesson-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // prevent default form submit
    document.getElementById("add-lesson-btn").style.pointerEvents = "none"; // prevent double submit

    // フォームのデータを取得
    const formData = new FormData(document.getElementById("add-lesson-form"));
    
    const sendingData = {
        year: formData.get("year"),
        season: formData.get("season"),
        number: formData.get("number"),
        title: formData.get("title"),
        teacher: formData.get("teacher"),
        day: formData.get("day"),
        time: formData.get("time"),
        price: formData.get("price"),
        description: formData.get("description"),
    };

    // エンドポイントにPOSTリクエストを送信
    const token = loadAccessToken();

    const response = await fetch("/lessons", {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
        body: JSON.stringify(sendingData),
    });

    if (response.ok) {
        const result = await response.json();
        console.log("Success:", result);
        fetchAndDisplayLessons();
    } else {
        console.error("Error on add lesson form");
    };

    // clear form after sending data
    document.querySelectorAll("#add-lesson-form > input").forEach(function (x) {
        x.value = "";
    });
    // reactivate submit button
    document.querySelector("#add-lesson-btn").style.pointerEvents = "auto";
});

