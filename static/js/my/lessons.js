// lessons.js


// function: get lesson list data depending on user
async function fetchLessons() {
    const token = loadAccessToken();
    const response = await fetch("/json/my/lessons", {
        method: "GET",
        headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
    });
    if (response.ok) {
        const result = await response.json();
        console.log("success: fetchLessons()");
        renderOnLogin();
        return result;
    } else {
        // throw new Error(`HTTP error! Status: ${response.status}`);
        console.error("error: fetchLessons()");
        renderOnLogout();
        return []; // empty <=> length == 0
    };
};



// function: render lesson list
async function renderLessons() {
    const lessons = await fetchLessons();
    const lessonList = document.getElementById("lesson-list");
    // clear the previous lesson list
    lessonList.textContent = "";

    lessons.forEach(function (lesson) {
        const listItem = `
            <li class="lesson-list-li flex-column">
                <div class="flex-row-between lesson-number-etc">
                    <div class="lesson-number"><div>${lesson.number}</div></div>
                    <div class="lesson-name"><div class="flex-row">${lesson.title}</div></div>
                    <div class="lesson-day">${lesson.day}</div>
                </div>

                <div class="flex-row lesson-img-etc">
                    <div class="lesson-img">img</div>
                    
                    <div class="lesson-time-etc" class="flex-column">
                        <div class="lesson-time">${lesson.time}</div>
                        <div class="lesson-place">${lesson.place}</div>
                        <div class="lesson-fee">${lesson.price}（全10回分）</div>
                        <div class="see-details"><a href="#">see details ></a></div>
                    </div>
                </div>

                <p class="lesson-description">${lesson.description}</p>

                <button class="lesson-sign-up-btn">申し込みをする</button>
            </li>
        `;
        lessonList.insertAdjacentHTML("beforeend", listItem);
    });
    if (lessons.length !== 0) {
        console.log("rendered lesson list");
    };
};



// function: attach event listeners to dynamically created elements
function attachEventListeners() {
    toggleIsDoneEventListeners();
    patchLessonEventListeners();
    deleteLesson();
};



// function: fetch and render lesson list data and attach event listeners
async function fetchAndDisplayLessons() {
    await renderLessons();
    attachEventListeners();
};



// on loading page: fetch and render lesson list
document.addEventListener("DOMContentLoaded", function () {
    //setDarkMode();
    fetchAndDisplayLessons();
});



// function: patch: toggle is_done
async function toggleIsDone(lessonId, sendingData) {
    await fetch(`/lessons/is-done/${lessonId}`, {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(sendingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
};


// function: attach toggle is_done event listeners
function toggleIsDoneEventListeners() {
    document.querySelectorAll(".toggle-status-btn").forEach( function (button) {
        button.addEventListener("click", async function () {
            const lessonId = this.dataset.lessonId;
            const currentIsDone = this.dataset.isDone === "true" ? true : false; // small letter "true"

            const sendingData = {
                is_done: !currentIsDone
            };
            
            console.log("fetching data...");
            await toggleIsDone(lessonId, sendingData);

            fetchAndDisplayLessons();
            console.log("success: rendered data.");
        });
    });
};



// function: patch a lesson
async function patchLesson(lessonId, sendingData) {
    const response = await fetch(`/lessons/${lessonId}`, {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(sendingData)
    });
    if (response.ok) {
        const result = await response.json();
        console.log("Success:", result);
    } else {
        console.error("Error: patchLesson()");
    };
};


// function: event listeners for "patchLesson" 
function patchLessonEventListeners() {
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            const lessonId = this.dataset.lessonId;
            const editForm = document.querySelector(`.edit-form[data-lesson-id="${lessonId}"]`);

            editForm.classList.toggle("hidden");
            
            // send patch request and refresh on click "Save" button
            editForm.querySelector(".confirm-edit-btn").addEventListener("click", async function () {
                const newTitle = editForm.querySelector(".edit-title").value;
                const newContent = editForm.querySelector(".edit-content").value;
                
                const sendingData = {};
                
                if (newTitle) {
                    sendingData.title = newTitle;
                }
                sendingData.content = newContent;
                
                console.log('fetching data...');
                await patchLesson(lessonId, sendingData);
                
                fetchAndDisplayLessons();
                console.log('rendered data.');
            });

            // hide this edit form on click "Cancel" button
            editForm.querySelector(".cancel-edit-btn").addEventListener("click", function () {
                editForm.classList.add("hidden");
            });
        });
    });
};





// function: delete lesson
function deleteLesson() {
    document.querySelectorAll(".delete-btn").forEach(function (button) {
        button.addEventListener("click", function () {
            const deleteForm = document.querySelector(`.delete-form[data-lesson-id="${lessonId}"]`);
            const lessonId = this.dataset.lessonId;

            deleteForm.classList.toggle("hidden");
            
            // send delete request and refresh on click "Confirm" button
            deleteForm.querySelector(".confirm-delete-btn").addEventListener("click", async function () {
                
                console.log("fetching data...");
                const response = await fetch(`/my/lessons/${lessonId}`, {
                    method: "DELETE"
                });
                if (response.ok) {
                    result = await response.json();
                    console.log("success:", result);
                } else {
                    console.error("error on deleteLessons()");
                };

                fetchAndDisplayLessons();
                console.log("rendered data.");
            });

            // hide this confirmation message on click "Cancel" button
            deleteForm.querySelector(".cancel-delete-btn").addEventListener("click", function () {
                deleteForm.classList.add("hidden");
            });
        });
    });
};




// create: add lesson => DONE
document.querySelectorAll(".add-lesson-btn").forEach(function (button) {
    button.addEventListener("submit", async function (event) {
        event.preventDefault(); // prevent default form submit
        document.querySelector(".add-lesson-btn").style.pointerEvents = "none"; // prevent double submit

        const lessonId = this.dataset.lessonId;
        
        const sendingData = {};

        // エンドポイントにPOSTリクエストを送信
        const token = loadAccessToken();
        const response = await fetch(`/my/lessons${lessonId}`, {
            method: "POST",
            headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
            body: JSON.stringify(sendingData)
        });
        if (response.ok) {
            const result = await response.json();
            console.log("Success:", data);
            fetchAndDisplayLessons();
            return result;
        } else {
            console.error("Error:", error);
        };
        // reactivate submit button
        document.querySelector(".add-lesson-btn").style.pointerEvents = "auto";
    });
});




// login form
document.getElementById("login-form").addEventListener('submit', async function (event) {
    event.preventDefault();
    document.getElementById("login-btn").style.pointerEvents = "none"; // prevent double submit
    const loginForm = document.getElementById("login-form");
    
    const formData = new FormData(loginForm);
    const username = formData.get('username');
    const password = formData.get('password');

    // ログインはjsonでなくform dataを送信する
    const response = await fetch('/token', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `username=${username}&password=${password}`,
    });

    if (response.ok) {
        const { access_token } = await response.json(); // { access_token } <=> response.access_token
        localStorage.setItem("accessToken", access_token);
        localStorage.setItem("username", username);
        
        location.reload();
        // alert('ログイン成功');
        console.log('success: login');
    } else {
        alert("error: login");
    }
    // reactivate submit button
    document.getElementById("login-btn").style.pointerEvents = "auto";
});


// logout
document.getElementById("logout-btn").addEventListener("click", async function (event) {
    event.preventDefault();
    localStorage.removeItem("accessToken");
    localStorage.removeItem("username");
    console.log("success: logout");
    alert("ログアウトしました。");
    location.reload();
});


// textareaの高さを自動調整
function autoResize(textarea) {
    // 高さを設定してからスクロールの有無をチェック
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
};



// load access token from local storage
function loadAccessToken() {
    try {
        const token = localStorage.getItem("accessToken");
        return token;
    } catch (error) {
        console.error("Failed to load access token", error);
    };
};




// sign up form
document.getElementById("sign-up-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // prevent the default form sending
    const signUpForm = document.getElementById("sign-up-form");

    // get the form data and define the sending data
    const formData = new FormData(signUpForm);
    
    const sendingData = {
        username: formData.get("username"),
        plain_password: formData.get("password")
    };
    
    // send a post request to the endpoint
    await fetch("/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(sendingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("success: create a new account", data);
        location.reload();
    })
    .catch((error) => {
        console.error("error: create a new account", error);
    });
});



// switch rendering depending on login status: logout
function renderOnLogout () {
    document.querySelectorAll(".on-login").forEach(function(x) {
        x.classList.add("hidden");
    });
    document.querySelectorAll(".on-logout").forEach(function(x) {
        x.classList.remove("hidden");
    });
};



// switch rendering depending on login status: login
function renderOnLogin () {
    document.querySelectorAll(".on-login").forEach(function(x) {
        x.classList.remove("hidden");
    });
    document.querySelectorAll(".on-logout").forEach(function(x) {
        x.classList.add("hidden");
    });
};


// function isDarkMode() {
//     const isDarkMode = localStorage.getItem("isDarkMode");
//     return isDarkMode;
// };


// function: set dark mode adaptively
function setDarkMode() {
    const isDarkMode = localStorage.getItem("isDarkMode");

    if (isDarkMode === "true") {
        document.body.classList.add("dark-mode");
        console.log("success: set dark mode");
    } else if (isDarkMode === "false") {
        // pass
        console.log("success: set light mode");
    } else {
        adaptiveDarkMode();
    };
};


// lemma: function for setDarkMode()
function adaptiveDarkMode() {
    const isDarkMode = window.matchMedia("(prefers-color-scheme:dark)").matches;

    if (isDarkMode === true) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("isDarkMode", true);
        console.log("success: saved dark mode");
    } else if (isDarkMode === false) {
        localStorage.setItem("isDarkMode", false);
        console.log("success: saved light mode");
    };
};


// switch dark mode and light mode
function toggleDarkMode() {
    const isDarkMode = document.body.classList.contains("dark-mode");

    if (isDarkMode) {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("isDarkMode", false);
    } else if (!isDarkMode) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("isDarkMode", true);
    };
};


// event listener to toggleDarkMode()
document.getElementById("toggle-dark-mode-btn").addEventListener("click", function () {
    toggleDarkMode();
});


