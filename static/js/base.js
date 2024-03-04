// base.js


// textareaの高さを自動調整
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
};


document.getElementById("user-btn").addEventListener("click", function () {
    document.getElementById("logout-btn").classList.toggle("hidden");
});


document.getElementById("menu-btn").addEventListener("click", function () {
    document.getElementById("nav-mobile-content").classList.toggle("hidden");
});




// switch rendering depending on login status: logout
function renderOnLogout () {
    document.querySelectorAll(".on-login").forEach(function (x) {
        x.classList.add("hidden");
    });
    document.querySelectorAll(".on-logout").forEach(function (x) {
        x.classList.remove("hidden");
    });
};



// switch rendering depending on login status: login
function renderOnLogin () {
    document.querySelectorAll(".on-login").forEach(function (x) {
        x.classList.remove("hidden");
    });
    document.querySelectorAll(".on-logout").forEach(function (x) {
        x.classList.add("hidden");
    });
};


