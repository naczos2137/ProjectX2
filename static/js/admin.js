const resetBtn = document.getElementById("resetBtn");
const roundBtn = document.getElementById("roundBtn");
const lobbyBtn = document.getElementById("lobbyBtn");
const statusDiv = document.getElementById("status");

function setStatus(text) {
    statusDiv.textContent = text;
}

// 🔥 reset gry
resetBtn.addEventListener("click", async () => {
    setStatus("Resetowanie...");

    await fetch("/admin/reset", {
        method: "POST"
    });

    setStatus("Gra zresetowana");
});

// 🔥 nowa tura
roundBtn.addEventListener("click", async () => {
    setStatus("Start nowej tury...");

    await fetch("/admin/new_round", {
        method: "POST"
    });

    setStatus("Nowa tura rozpoczęta");
});

// 🔥 do lobby
lobbyBtn.addEventListener("click", async () => {
    setStatus("Powrót do lobby...");

    await fetch("/admin/lobby", {
        method: "POST"
    });

    setStatus("Wrócono do lobby");
});