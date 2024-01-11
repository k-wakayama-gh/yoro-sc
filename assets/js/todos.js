// todos.js

// Create
document.getElementById("add-todo-form").addEventListener("submit", function(event) {
    event.preventDefault(); // フォームのデフォルトの送信を停止

    // フォームのデータを取得
    const formData = new FormData(document.getElementById("add-todo-form"));
    
    // データをオブジェクトに変換し、titleとcontentを文字列に変換
    const todoData = {
        title: String(formData.get("title")),
        content: String(formData.get("content"))
    };

    // FastAPIのエンドポイントにPOSTリクエストを送信
    fetch("/todos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(todoData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        // リクエストが成功したらページをリロード
        location.reload();
    })
    .catch((error) => {
        console.error("Error:", error);
        // エラーが発生した場合の処理を追加
    });
});





// ToDoリスト内のToggle Statusボタンをクリックした時の処理
document.querySelectorAll(".toggle-status-btn").forEach(button => {
    button.addEventListener("click", async function(event) {
        const todoId = this.dataset.todoId; // ボタンに紐付けられたToDoのIDを取得
        const currentIsDone = this.dataset.isDone === "True" ? true : false; // 現在のis_doneの状態を取得

        // FastAPIのエンドポイントにPATCHリクエストを送信してステータスをトグルする
        await fetch(`/todos/${todoId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ is_done: !currentIsDone }) // 現在の状態を反転して送信する
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
            // リクエストが成功した場合の処理を追加
            // 例: ステータスをトグルした後の表示を更新する
            document.location.reload(); // 必要に応じてページ全体をリロードする
        })
        .catch((error) => {
            console.error("Error:", error);
            // エラーが発生した場合の処理を追加
        });
    });
});





// ToDoリスト内のEditボタンをクリックした時の処理
document.querySelectorAll(".edit-btn").forEach(button => {
    button.addEventListener("click", function(event) {
        const todoId = this.dataset.todoId; // Editボタンに紐付けられたToDoのIDを取得

        // ToDoの内容を表示している要素を非表示にし、編集用フォームを表示する
        const todoElement = document.querySelector(`li[data-todo-id="${todoId}"]`);
        // todoElement.classList.add("hidden");

        const editForm = document.querySelector(`.edit-form[data-todo-id="${todoId}"]`);
        editForm.classList.toggle("hidden");

        // 編集用フォーム内のSaveボタンがクリックされた時の処理
        editForm.querySelector(".confirm-edit-btn").addEventListener("click", function() {
            const newTitle = editForm.querySelector(".edit-title").value;
            const newContent = editForm.querySelector(".edit-content").value;

            // FastAPIのエンドポイントにPATCHリクエストを送信してToDoを更新
            fetch(`/todos/${todoId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: newTitle,
                    content: newContent
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
                // リクエストが成功したらToDoリストを更新
                document.location.reload();
            })
            .catch((error) => {
                console.error("Error:", error);
                // エラーが発生した場合の処理を追加
            });
        });

        // 編集用フォーム内のCancelボタンがクリックされた時の処理
        editForm.querySelector(".cancel-edit-btn").addEventListener("click", function() {
            // 編集用フォームを非表示にし、ToDoの内容を表示している要素を再表示する
            editForm.classList.add("hidden");
            // todoElement.classList.remove("hidden");
        });
    });
});




// ToDoリスト内の削除ボタンをクリックした時の処理
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
                // リクエストが成功したらToDoリストを更新
                // 例: ページをリロード
                document.location.reload();
            })
            .catch((error) => {
                console.error("Error:", error);
                // エラーが発生した場合の処理を追加
            });
        });

        // 確認用ポップアップ内のCancelボタンがクリックされた時の処理
        confirmationPopup.querySelector(".cancel-delete-btn").addEventListener("click", function() {
            // 確認用ポップアップを隠す
            confirmationPopup.classList.add("hidden");
        });
    });
});




// ログインフォーム
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const formData = new FormData(loginForm);
    const username = formData.get('username');
    const password = formData.get('password');

    const response = await fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&password=${password}`,
    });

    if (response.ok) {
        const { access_token } = await response.json();
        // トークンをlocalStorageなどに保存
        localStorage.setItem('accessToken', access_token);
        alert('ログイン成功');
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


