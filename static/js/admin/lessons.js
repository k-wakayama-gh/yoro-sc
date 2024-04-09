// admin/lessons.js

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
        capacity: formData.get("capacity"),
        lessons: formData.get("lessons"),
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




// on loading page: fetch and render lesson list
document.addEventListener("DOMContentLoaded", function () {
    //setDarkMode();
    fetchAndDisplayLessons();
});


// fetch, render lesson list data and attach event listeners
async function fetchAndDisplayLessons() {
    await renderLessons();
    attachEventListeners();
};


// attach event listeners to dynamically created elements
function attachEventListeners() {
    signUpLesson();
    cancelLessonOnSmallBtn();
};



// render lesson list
async function renderLessons() {
    const lessons = await fetchLessons();
    const myLessons = await fetchMyLessons();
    const lessonList = document.getElementById("lesson-list");

    // clear the previous lesson list
    lessonList.textContent = "";

    const cancelBtn = `<span class="lesson-cancel-btn-small" onclick="cancelLessonOnSmallBtn()">キャンセル</span>`;

    lessons.forEach(function (lesson) {
        let signUpBtn = "";
        if (document.getElementById("user-btn").classList.contains("is-loged-out")) {
            signUpBtn = "";
        } else if (myLessons.some(myLesson => myLesson.id == lesson.id)) {
            signUpBtn = `<button class="dummy-btn" style="position: relative;">申し込み済み${cancelBtn}</button>`;
        } else {
            signUpBtn = `<button class="lesson-sign-up-btn">申し込みをする</button>`;
        };
        let numberColor = "gray";
        if (lesson.number <= 1) {
            numberColor = "#a44d3a";
        } else {
            numberColor = "#4379a6";
        };
        let capacity_left = lesson.capacity;
        if (lesson.capacity_left != null) {
            capacity_left = lesson.capacity_left;
        };
        let capacity = "なし";
        if (lesson.capacity != null) {
            capacity = capacity_left + " / " + lesson.capacity + " 名";
        };
        const dayColor = {"日": "red", "月": "gray", "火": "orange", "水": "#4193f6", "木": "3f8d57", "金": "#f19937", "土": "blue"};
        const listItem = `
            <li class="lesson-list-li flex-column" style="border-color: ${numberColor};" data-lesson-id="${lesson.id}">
                <div class="flex-row-between lesson-number-etc">
                    <div class="lesson-number" style="background-color: ${numberColor};"><div>${lesson.number}</div></div>
                    <div class="lesson-name"><div class="flex-row">${lesson.title}</div></div>
                    <div class="lesson-day" style="background-color: ${dayColor[lesson.day]};">${lesson.day}</div>
                </div>

                <div class="flex-row lesson-img-etc">
                    <div class="lesson-teacher-etc flex-column">
                        <div class="lesson-img"><img src="/static/img/lessons/${lesson.teacher}.png"></div>
                        <div class="lesson-teacher"><span class="lesson-teacher-name">講師　</span>${lesson.teacher}</div>
                    </div>
                    
                    <div class="lesson-time-etc flex-column">
                        <div class="lesson-time">${lesson.time}</div>
                        <div class="lesson-fee">${lesson.price.toLocaleString()}円（全${lesson.lessons}回分）</div>
                        <div class="lesson-capacity">定員残り ${capacity}</div>
                        <!-- <div class="see-details"><a href="#">詳しく見る ＞</a></div> -->
                    </div>
                </div>

                <p class="lesson-description">${lesson.description}</p>

                ${signUpBtn}
            </li>
        `;
        lessonList.insertAdjacentHTML("beforeend", listItem);
    });
    if (lessons.length !== 0) {
        console.log("rendered lesson list");
        const poster = `<li class="lesson-poster"><img src="/static/img/lessons/lesson-poster.png" style="width:100%; height: auto;"></li>`;
        document.querySelector("#lesson-list > :nth-child(1)").insertAdjacentHTML("afterend", poster);
    };
};




// get lessons
async function fetchLessons() {
    const token = loadAccessToken();
    const response = await fetch("/json/admin/lessons", {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
    });
    if (response.ok) {
        const lessons = await response.json();
        console.log("success: fetchLessons()", lessons);
        // renderOnLogin();
        return lessons;
    } else {
        console.error("error: fetchLessons()");
        document.querySelector(".not-allowed").classList.remove("hidden");
        return []; // empty <=> length == 0
    };
};




// get my lessons
async function fetchMyLessons() {
    const token = loadAccessToken();
    const response = await fetch("/json/my/lessons", {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
    });
    if (response.ok) {
        const myLessons = await response.json();
        console.log("success: fetchMyLessons()", myLessons);
        return myLessons;
    } else {
        console.error("error: fetchMyLessons()");
        return []; // empty <=> length == 0
    };
};




// sign up to a lesson
function signUpLesson() {
    document.querySelectorAll(".lesson-sign-up-btn").forEach(function (button) {
        button.addEventListener("click", async function () {
            const token = loadAccessToken();
            const lessonId = this.parentNode.dataset.lessonId;

            this.textContent = "処理中...";

            const body = {};

            console.log("fetching data...");

            const response = await fetch(`/lessons/${lessonId}`, {
                method: "POST",
                headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const result = await response.json();
                fetchAndDisplayLessons();
                console.log("success: signed up to a lesson", result);
            } else {
                console.error("error: signUpLesson()");
                alert("エラーが発生しました。もう一度やり直してください。")
            };
        });
    });
};



// sign up to a children lesson
function signupChildrenLesson() {
    console.log("aaa")
};



// cancel a lesson
function cancelLessonOnSmallBtn() {
    document.querySelectorAll(".lesson-cancel-btn-small").forEach(function (button) {
        button.addEventListener("click", async function () {
            const token = loadAccessToken();
            const lessonId = this.parentNode.parentNode.dataset.lessonId;

            this.parentNode.textContent = "処理中...";
            this.textContent = "";

            const body = {};

            console.log("fetching data...");

            const response = await fetch(`/my/lessons/${lessonId}`, {
                method: "DELETE",
                headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const result = await response.json();
                fetchAndDisplayLessons();
                console.log("success: cancel a lesson", result);
            } else {
                console.error("error: cancelLesson()");
            };
        });
    });
};

