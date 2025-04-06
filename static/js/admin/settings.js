// admin/settings.js

// フォーム送信時の処理
document.getElementById("period-form").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    // フォームのデータを取得
    const year = document.getElementById("year").value;
    const season = document.getElementById("season").value;
    const start_time = document.getElementById("start_time").value;
    const end_time = document.getElementById("end_time").value;
  
    // PeriodRequestオブジェクトを作成
    const periodRequest = {
      year: parseInt(year),
      season: parseInt(season),
      start_time: convertToDateDict(start_time),
      end_time: convertToDateDict(end_time)
    };
  
    // トークンを取得して、Authorizationヘッダーに設定
    const token = loadAccessToken();
  
    if (!token) {
      alert("トークンが見つかりません。");
      return;
    }
  
    const response = await fetch("/admin/period", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify(periodRequest)
    });
  
    if (response.ok) {
        const result = await response.json();
        document.getElementById("response-message").textContent = "期間情報が更新されました。";
        } else {
        const error = await response.json();
        document.getElementById("response-message").textContent = "エラー: " + error.detail;
        }
});

function convertToDateDict(dateTimeString) {
    const date = new Date(dateTimeString);
  
    return {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes(),
      timezone: 9  // JST
    };
};

