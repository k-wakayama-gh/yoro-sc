// lessons.js


// function: get lesson list data for the current year and season
async function fetchLessons() {
    const response = await fetch("/json/lessons", {
        method: "GET",
        headers: {"Content-Type": "application/json"},
    });
    if (response.ok) {
        const lessons = await response.json();
        console.log("success: fetchLessons()");
        // renderOnLogin();
        return lessons;
    } else {
        console.error("error: fetchLessons()");
        // renderOnLogout();
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
                        <div class="lesson-fee">${lesson.price}円（全10回分）</div>
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
    //;
};



// function: fetch and render lesson list data and attach event listeners
async function fetchAndDisplayLessons() {
    await renderLessons();
    // attachEventListeners();
};



// on loading page: fetch and render lesson list
document.addEventListener("DOMContentLoaded", function () {
    //setDarkMode();
    fetchAndDisplayLessons();
});



// // function: patch: toggle is_done
// async function toggleIsDone(lessonId, sendingData) {
//     await fetch(`/lessons/is-done/${lessonId}`, {
//         method: "PATCH",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(sendingData)
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log("Success:", data);
//     })
//     .catch((error) => {
//         console.error("Error:", error);
//     });
// };


// // function: attach toggle is_done event listeners
// function toggleIsDoneEventListeners() {
//     document.querySelectorAll(".toggle-status-btn").forEach( function (button) {
//         button.addEventListener("click", async function () {
//             const lessonId = this.dataset.lessonId;
//             const currentIsDone = this.dataset.isDone === "true" ? true : false; // small letter "true"

//             const sendingData = {
//                 is_done: !currentIsDone
//             };
            
//             console.log("fetching data...");
//             await toggleIsDone(lessonId, sendingData);

//             fetchAndDisplayLessons();
//             console.log("success: rendered data.");
//         });
//     });
// };



// // function: patch a lesson
// async function patchLesson(lessonId, sendingData) {
//     const response = await fetch(`/lessons/${lessonId}`, {
//         method: "PATCH",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(sendingData)
//     });
//     if (response.ok) {
//         const result = await response.json();
//         console.log("Success:", result);
//     } else {
//         console.error("Error: patchLesson()");
//     };
// };


// // function: event listeners for "patchLesson" 
// function patchLessonEventListeners() {
//     document.querySelectorAll(".edit-btn").forEach(button => {
//         button.addEventListener("click", function () {
//             const lessonId = this.dataset.lessonId;
//             const editForm = document.querySelector(`.edit-form[data-lesson-id="${lessonId}"]`);

//             editForm.classList.toggle("hidden");
            
//             // send patch request and refresh on click "Save" button
//             editForm.querySelector(".confirm-edit-btn").addEventListener("click", async function () {
//                 const newTitle = editForm.querySelector(".edit-title").value;
//                 const newContent = editForm.querySelector(".edit-content").value;
                
//                 const sendingData = {};
                
//                 if (newTitle) {
//                     sendingData.title = newTitle;
//                 }
//                 sendingData.content = newContent;
                
//                 console.log('fetching data...');
//                 await patchLesson(lessonId, sendingData);
                
//                 fetchAndDisplayLessons();
//                 console.log('rendered data.');
//             });

//             // hide this edit form on click "Cancel" button
//             editForm.querySelector(".cancel-edit-btn").addEventListener("click", function () {
//                 editForm.classList.add("hidden");
//             });
//         });
//     });
// };





// // function: delete lesson
// function deleteLesson() {
//     document.querySelectorAll(".delete-btn").forEach(function (button) {
//         button.addEventListener("click", function () {
//             const deleteForm = document.querySelector(`.delete-form[data-lesson-id="${lessonId}"]`);
//             const lessonId = this.dataset.lessonId;

//             deleteForm.classList.toggle("hidden");
            
//             // send delete request and refresh on click "Confirm" button
//             deleteForm.querySelector(".confirm-delete-btn").addEventListener("click", async function () {
                
//                 console.log("fetching data...");
//                 const response = await fetch(`/my/lessons/${lessonId}`, {
//                     method: "DELETE"
//                 });
//                 if (response.ok) {
//                     result = await response.json();
//                     console.log("success:", result);
//                 } else {
//                     console.error("error on deleteLessons()");
//                 };

//                 fetchAndDisplayLessons();
//                 console.log("rendered data.");
//             });

//             // hide this confirmation message on click "Cancel" button
//             deleteForm.querySelector(".cancel-delete-btn").addEventListener("click", function () {
//                 deleteForm.classList.add("hidden");
//             });
//         });
//     });
// };




// // create: add lesson => DONE
// document.querySelectorAll(".add-lesson-btn").forEach(function (button) {
//     button.addEventListener("submit", async function (event) {
//         event.preventDefault(); // prevent default form submit
//         document.querySelector(".add-lesson-btn").style.pointerEvents = "none"; // prevent double submit

//         const lessonId = this.dataset.lessonId;
        
//         const sendingData = {};

//         // エンドポイントにPOSTリクエストを送信
//         const token = loadAccessToken();
//         const response = await fetch(`/my/lessons${lessonId}`, {
//             method: "POST",
//             headers: {"Content-Type": "application/json", "Authorization": "Bearer " + token},
//             body: JSON.stringify(sendingData)
//         });
//         if (response.ok) {
//             const result = await response.json();
//             console.log("Success:", data);
//             fetchAndDisplayLessons();
//             return result;
//         } else {
//             console.error("Error:", error);
//         };
//         // reactivate submit button
//         document.querySelector(".add-lesson-btn").style.pointerEvents = "auto";
//     });
// });





// function isDarkMode() {
//     const isDarkMode = localStorage.getItem("isDarkMode");
//     return isDarkMode;
// };


