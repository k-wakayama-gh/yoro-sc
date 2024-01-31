// todos2.js

// Event Delegation for todo-action-section
document.getElementById("todo-list").addEventListener("click", function(event) {
    const target = event.target;

    if (target.classList.contains("toggle-status-btn")) {
        handleToggleStatusButtonClick(target);
    } else if (target.classList.contains("edit-btn")) {
        handleEditButtonClick(target);
    } else if (target.classList.contains("delete-btn")) {
        handleDeleteButtonClick(target);
    }
});


// function: read: ToDo list data async
async function fetchTodos() {
    try {
        const response = await fetch("/todos/json");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        };

        const todos = await response.json();
        return todos;
    } catch (error) {
        console.error("Error fetching data:", error);
        return [];
    }
};



// Updated displayTodos function
function displayTodos(todos) {
    const todoList = document.getElementById("todo-list");
    todoList.textContent = ""; // 既存のToDoをクリア

    todos.forEach((todo) => {
        const listItem = `
            <li>
                <strong>${todo.title}</strong>
                ${todo.content ? `<p>${todo.content}</p>` : ''}
                <p>Status: ${todo.is_done ? 'Done' : 'Pending'}</p>
                <section class="todo-action-section">
                    <!-- Pending状態変更ボタン -->
                    <button class="toggle-status-btn" data-todo-id="${ todo.id }" data-is-done="${ todo.is_done }">Toggle Status</button>
                    <!-- Editボタン -->
                    <button class="edit-btn" data-todo-id="${todo.id}">Edit</button>
                    <!-- Deleteボタン -->
                    <button class="delete-btn" data-todo-id="${todo.id}">Delete</button>
                    <!-- 確認用メッセージ -->
                    <div class="delete-form hidden" data-todo-id="${todo.id}">
                        <p>Are you sure you want to delete this ToDo?</p>
                        <button class="confirm-delete-btn">Confirm</button>
                        <button class="cancel-delete-btn">Cancel</button>
                    </div>
                    <!-- Editフォーム -->
                    <div class="edit-form hidden" data-todo-id="${todo.id}">
                        <input type="text" class="edit-title" placeholder="New Title" value="${todo.title}">
                        <textarea class="edit-content" placeholder="New Content" oninput="autoResize(this)">${todo.content}</textarea>
                        <button class="confirm-edit-btn">Save</button>
                        <button class="cancel-edit-btn">Cancel</button>
                    </div>
                </section>
            </li>
        `;
        todoList.insertAdjacentHTML("beforeend", listItem);
    });

    // Attach event listeners after elements are added to the DOM
    attachEventListeners();
}



// function: fetch and display todo list data
async function fetchAndDisplayTodos() {
    const todos = await fetchTodos();
    displayTodos(todos);
    attachEventListeners();
};


// ページロード時にToDoリストのデータを非同期で取得・表示する
document.addEventListener("DOMContentLoaded", async function () {
    fetchAndDisplayTodos();
});




// create: add todo from
document.getElementById("add-todo-form").addEventListener("submit", function(event) {
    event.preventDefault(); // フォームのデフォルトの送信を停止

    // フォームのデータを取得
    const formData = new FormData(document.getElementById("add-todo-form"));
    
    const sendingData = {
        title: formData.get("title"),
        content: formData.get("content")
    };

    // エンドポイントにPOSTリクエストを送信
    fetch("/todos", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(sendingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        // location.reload();
        fetchAndDisplayTodos();
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});



// Attach event listeners to dynamically created elements
function attachEventListeners() {
    // Toggle Status
    document.querySelectorAll(".toggle-status-btn").forEach(button => {
        button.addEventListener("click", async function(event) {
            const todoId = this.dataset.todoId; // ボタンに紐付けられたToDoのIDを取得
            const currentIsDone = this.dataset.isDone === "True" ? true : false; // 現在のis_doneの状態を取得
            
            // 送信するデータは現在の状態の反転
            const sendingData = {
                is_done: !currentIsDone
            };

            // エンドポイントにPATCHリクエストを送信する
            await fetch(`/todos/is-done/${todoId}`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(sendingData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
                // document.location.reload();
                fetchAndDisplayTodos();
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    });

    // Edit
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            const todoId = this.dataset.todoId; // Editボタンに紐付けられたToDoのIDを取得
            
            // 編集用のフォームを表示する
            const editForm = document.querySelector(`.edit-form[data-todo-id="${todoId}"]`);
            editForm.classList.toggle("hidden");

            // 編集用フォーム内のSaveボタンがクリックされた時の処理
            editForm.querySelector(".confirm-edit-btn").addEventListener("click", function() {
                const newTitle = editForm.querySelector(".edit-title").value;
                const newContent = editForm.querySelector(".edit-content").value;

                // 送信するデータを格納するオブジェクト
                const sendingData = {};

                // 新しいデータが存在すればオブジェクトに追加 => contentはNone/Nullでもいい
                if (newTitle) {
                    sendingData.title = newTitle;
                }
                // if (newContent) {
                //     sendingData.content = newContent;
                // }
                sendingData.content = newContent;

                // エンドポイントにPATCHリクエストを送信する
                fetch(`/todos/${todoId}`, {
                    method: "PATCH",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(sendingData)
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Success:", data);
                    // document.location.reload();
                    fetchAndDisplayTodos();
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
            });

            // 編集用フォーム内のCancelボタンがクリックされた時の処理
            editForm.querySelector(".cancel-edit-btn").addEventListener("click", function() {
                // 編集用フォームを非表示にする
                editForm.classList.add("hidden");
            });
        });
    });

    // Delete
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            const todoId = this.dataset.todoId; // 削除ボタンに紐付けられたToDoのIDを取得

            // 確認用ポップアップを表示
            const confirmationPopup = document.querySelector(`.confirmation-popup[data-todo-id="${todoId}"]`);
            confirmationPopup.classList.toggle("hidden");

            // 確認用ポップアップ内のConfirmボタンがクリックされた時の処理
            confirmationPopup.querySelector(".confirm-delete-btn").addEventListener("click", function() {
                // FastAPIのエンドポイントにDELETEリクエストを送信してToDoを削除
                fetch(`/todos/${todoId}`, {
                    method: "DELETE"
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Success:", data);
                    // document.location.reload();
                    fetchAndDisplayTodos();
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
            });

            // 確認用メッセージのCancelボタンがクリックされた時の処理
            confirmationPopup.querySelector(".cancel-delete-btn").addEventListener("click", function() {
                // 確認用メッセージを隠す
                confirmationPopup.classList.add("hidden");
            });
        });
    });
}


// Initial fetch and display
document.addEventListener("DOMContentLoaded", async function() {
    await fetchAndDisplayTodos();
    // Attach event listeners after initial display
    attachEventListeners();
});


// ログインフォーム
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
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
        const { access_token } = await response.json();
        // トークンをlocalStorageに保存
        localStorage.setItem('accessToken', access_token);
        alert('ログイン成功');
        // console.log('ログイン成功');
    } else {
        alert('ログイン失敗');
    }
});


// ログアウト
const logoutBtn = document.getElementById('logout-btn');
logoutBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    localStorage.removeItem('accessToken');
    }
);


// textareaの高さを自動調整
function autoResize(textarea) {
    // 高さを設定してからスクロールの有無をチェック
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

