const avatarSelect = document.getElementById("avatarSelect");
const avatarImage = document.getElementById("avatarImage");
const form = document.getElementById("joinForm");

// ---------- AVATAR PREVIEW ----------

avatarSelect.addEventListener("change", () => {
    avatarImage.src = "/static/avatars/" + avatarSelect.value;
});

// ---------- FORM SUBMIT ----------

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nickname = document.getElementById("nickname").value;
    const avatar = avatarSelect.value;
    let clientId = localStorage.getItem("client_id");

    if (!clientId) {
        clientId = Math.random().toString(36).slice(2);
        localStorage.setItem("client_id", clientId);
    }

    await fetch("/join", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            name: nickname,
            avatar: avatar
        })
    });

    window.location.href = "/lobby";
});
