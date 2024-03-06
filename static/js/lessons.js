// lessons.js


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
};




// render lesson list
async function renderLessons() {
    const lessons = await fetchLessons();
    const myLessons = await fetchMyLessons();
    const lessonList = document.getElementById("lesson-list");

    // clear the previous lesson list
    lessonList.textContent = "";

    lessons.forEach(function (lesson) {
        let signUpBtn = "";
        if (myLessons.some(myLesson => myLesson.id == lesson.id)) {
            signUpBtn = `<button class="dummy-btn">申し込み済み</button>`;
        } else {
            signUpBtn = `<button class="lesson-sign-up-btn">申し込みをする</button>`;
        };
        const listItem = `
            <li class="lesson-list-li flex-column" data-lesson-id="${lesson.id}">
                <div class="flex-row-between lesson-number-etc">
                    <div class="lesson-number"><div>${lesson.number}</div></div>
                    <div class="lesson-name"><div class="flex-row">${lesson.title}</div></div>
                    <div class="lesson-day">${lesson.day}</div>
                </div>

                <div class="flex-row lesson-img-etc">
                    <div class="lesson-img">img</div>
                    
                    <div class="lesson-time-etc" class="flex-column">
                        <div class="lesson-time">${lesson.time}</div>
                        <div class="lesson-fee">${lesson.price}円（全10回分）</div>
                        <div class="see-details"><a href="#">詳しく見る ＞</a></div>
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
    };
};




// get lessons
async function fetchLessons() {
    const response = await fetch("/json/lessons", {
        method: "GET",
        headers: {"Content-Type": "application/json"},
    });
    if (response.ok) {
        const lessons = await response.json();
        console.log("success: fetchLessons()", lessons);
        // renderOnLogin();
        return lessons;
    } else {
        console.error("error: fetchLessons()");
        // renderOnLogout();
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
        // renderOnLogin();
        return myLessons;
    } else {
        console.error("error: fetchMyLessons()");
        // renderOnLogout();
        return []; // empty <=> length == 0
    };
};




// sign up to a lesson
function signUpLesson() {
    document.querySelectorAll(".lesson-sign-up-btn").forEach(function (button) {
        button.addEventListener("click", async function () {
            const token = loadAccessToken();
            const lessonId = this.parentNode.dataset.lessonId;

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
                alert("教室の申し込みに失敗しました。ログインしてください。")
            };
        });
    });
};



