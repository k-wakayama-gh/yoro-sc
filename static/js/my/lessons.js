// my/lessons.js


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
    cancelLesson();
};



// render lesson list
async function renderLessons() {
    const myLessons = await fetchMyLessons();
    const lessonList = document.getElementById("lesson-list");

    // clear the previous lesson list
    lessonList.textContent = "";

    const dayColor = {"日": "red", "月": "gray", "火": "orange", "水": "#4193f6", "木": "3f8d57", "金": "#f19937", "土": "blue"};

    if (myLessons.length == 0) {
        lessonList.insertAdjacentHTML("afterend", "<p class='text-center'>現在申し込み済みの教室はありません。</p>");
    };

    myLessons.forEach(function (lesson) {
        let numberColor = "gray";
        if (lesson.number <= 1) {
            numberColor = "#a44d3a";
        } else {
            numberColor = "#4379a6";
        };
        const listItem = `
            <li class="lesson-list-li flex-column" style="border-color: ${numberColor};" data-lesson-id="${lesson.id}">
                <div class="flex-row-between lesson-number-etc">
                    <div class="lesson-number"  style="background-color: ${numberColor};"><div>${lesson.number}</div></div>
                    <div class="lesson-name"><div class="flex-row">${lesson.title}</div></div>
                    <div class="lesson-day" style="background-color: ${dayColor[lesson.day]};">${lesson.day}</div>
                </div>

                <div class="flex-row lesson-img-etc">
                    <div class="lesson-teacher-etc flex-column">
                        <div class="lesson-img"><img src="/static/img/lessons/${lesson.teacher}.png"></div>
                        <div class="lesson-teacher"><span class="lesson-teacher-name">講師　</span>${lesson.teacher}</div>
                    </div>
                    
                    <div class="lesson-time-etc" class="flex-column">
                        <div class="lesson-time">${lesson.time}</div>
                        <div class="lesson-fee">${lesson.price.toLocaleString()}円（全${lesson.lessons}回分）</div>
                        <!-- <div class="see-details"><a href="#">詳しく見る ＞</a></div> -->
                    </div>
                </div>

                <p class="lesson-description">${lesson.description}</p>

                <button class="lesson-cancel-btn hidden">キャンセルする</button>
            </li>
        `;
        lessonList.insertAdjacentHTML("beforeend", listItem);
    });
    if (myLessons.length !== 0) {
        console.log("rendered lesson list");
        document.getElementById("fee-list-section").classList.remove("hidden");
    };

    const feeList = document.getElementById("fee-list");
    feeList.textContent = "";
    let totalFee = 0;
    myLessons.forEach(function (lesson) {
        totalFee = totalFee + lesson.price;
        const fee = `<p>${lesson.title}：${lesson.price.toLocaleString()}円</p>`;
        feeList.insertAdjacentHTML("beforeend", fee);
    });
    // feeList.insertAdjacentHTML("beforeend", `<p style="font-weight: bold;">合計：${totalFee.toLocaleString()}円</p>`);
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




// cancel a lesson
function cancelLesson() {
    document.querySelectorAll(".lesson-cancel-btn").forEach(function (button) {
        button.addEventListener("click", async function () {
            const token = loadAccessToken();
            const lessonId = this.parentNode.dataset.lessonId;

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








// function isDarkMode() {
//     const isDarkMode = localStorage.getItem("isDarkMode");
//     return isDarkMode;
// };


